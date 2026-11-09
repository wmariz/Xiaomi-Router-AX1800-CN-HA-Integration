package com.wmariz.miwifipainel;

import android.content.Context;
import android.content.SharedPreferences;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.TreeSet;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Servidor local (127.0.0.1) equivalente ao desktop/painel.py: serve a página do painel
 * e repassa as chamadas à API interna (LuCI /api/...) dos roteadores.
 * A senha é usada só no login (hash SHA1 com nonce) e não é guardada.
 */
public class Servidor {
    public static final int PORTA = 8099;
    private static final String CHAVE_PADRAO = "a2ffa5c9be07488bbb04a3a47d3c5f6a";
    private static final Pattern IP_RE = Pattern.compile("^(25[0-5]|2[0-4]\\d|1?\\d?\\d)(\\.(25[0-5]|2[0-4]\\d|1?\\d?\\d)){3}$");
    private static final String[] PAGINAS = {
        "web/home", "web/setting/wifi", "web/setting/wan", "web/setting/lannetset",
        "web/setting/safe", "web/setting/upgrade", "web/apsetting/wifi", "web/store", "web/prosetting/qos"};
    private static final String[] EXTRAS = {
        "api/misns/wifi_share_info", "api/misystem/status", "api/misystem/sys_time",
        "api/xqnetwork/wan_info", "api/xqnetwork/wifi_detail_all", "api/misystem/devicelist",
        "api/misystem/topo_graph", "api/misystem/messages", "api/misystem/qos_info",
        "api/xqnetwork/get_son_backhaul_mode", "api/xqnetwork/get_miscan_switch",
        "api/xqnetwork/get_miotrelay_switch", "api/xqsystem/country_code"};
    private static final Pattern ESCRITA = Pattern.compile(
        "(^|/)(set_|add_|del|remove|reboot|reset|shutdown|upgrade|flash|login|logout|"
        + "c_restore|c_upload|c_backup|bandwidth_test|scan_|qos_mode|qos_limit|qos_offlimit|qos_guest|"
        + "unbind|bind|apply|start|stop|clean|clear|format|repair|register|renew|grant|update|connect|"
        + "wps$|wps_cancel|iperf|speed_test$|ota$|password|disable|edit_|manually_|mac_clone|r_ip_conflict|"
        + "usb_u3|usbservice|usbmode|upload|web_access_opt|led$|netacctl_set|parctl_(add|delete|update)|request)"
        + "|switch", Pattern.CASE_INSENSITIVE);
    private static final Pattern SENSIVEIS = Pattern.compile("(pass|pwd|psk|key|token|stok|secret|sswd|senha)", Pattern.CASE_INSENSITIVE);
    private static final Pattern API_RE = Pattern.compile("api/[a-z_]+/[a-z_0-9]+", Pattern.CASE_INSENSITIVE);
    private static final Pattern SRC_RE = Pattern.compile("src=\"([^\"]+\\.js[^\"]*)\"");

    private final Context ctx;
    private final Runnable aoSair;
    private final Map<String, String> roteadores = Collections.synchronizedMap(new LinkedHashMap<String, String>());
    private final Map<String, String> sessoes = new ConcurrentHashMap<>();
    private final Map<String, JSONArray> cacheEndpoints = new ConcurrentHashMap<>();
    private final ExecutorService pool = Executors.newCachedThreadPool();
    private ServerSocket servidor;

    public Servidor(Context ctx, Runnable aoSair) {
        this.ctx = ctx;
        this.aoSair = aoSair;
        carregarCfg();
    }

    // ---------- configuração (endereços dos roteadores) ----------
    private SharedPreferences prefs() { return ctx.getSharedPreferences("miwifi", Context.MODE_PRIVATE); }

    private void carregarCfg() {
        roteadores.clear();
        try {
            JSONObject j = new JSONObject(prefs().getString("roteadores", "{}"));
            Iterator<String> it = j.keys();
            while (it.hasNext()) {
                String k = it.next(); String v = j.optString(k);
                if (IP_RE.matcher(v).matches()) roteadores.put(k, v);
            }
        } catch (Exception ignored) { }
        if (roteadores.isEmpty()) { roteadores.put("principal", "192.168.0.1"); roteadores.put("repetidor", "192.168.0.2"); }
    }

    private void salvarCfg() {
        prefs().edit().putString("roteadores", new JSONObject(new LinkedHashMap<>(roteadores)).toString()).apply();
    }

    // ---------- cliente HTTP/1.0 tolerante (o repetidor manda cabeçalhos malformados) ----------
    static final class Resp { int status; String corpo; }

    static Resp http(String url, byte[] dados) throws Exception { return http(url, dados, "application/x-www-form-urlencoded"); }

    /** Corpo multipart/form-data com o arquivo no campo 'image' (como a página oficial envia). */
    static Object[] multipart(JSONObject campos, JSONObject arquivo) throws Exception {
        String limite = "----miwifi" + Long.toHexString(System.nanoTime());
        ByteArrayOutputStream b = new ByteArrayOutputStream();
        if (campos != null) {
            java.util.Iterator<String> it = campos.keys();
            while (it.hasNext()) { String k = it.next();
                b.write(("--" + limite + "\r\nContent-Disposition: form-data; name=\"" + k + "\"\r\n\r\n" + campos.opt(k) + "\r\n").getBytes(StandardCharsets.UTF_8)); }
        }
        String nome = arquivo.optString("nome", "arquivo.bin").replace("\"", "");
        b.write(("--" + limite + "\r\nContent-Disposition: form-data; name=\"image\"; filename=\"" + nome + "\"\r\nContent-Type: application/octet-stream\r\n\r\n").getBytes(StandardCharsets.UTF_8));
        b.write(android.util.Base64.decode(arquivo.optString("b64", ""), android.util.Base64.DEFAULT));
        b.write(("\r\n--" + limite + "--\r\n").getBytes(StandardCharsets.UTF_8));
        return new Object[]{ b.toByteArray(), "multipart/form-data; boundary=" + limite };
    }

    static Resp http(String url, byte[] dados, String tipo) throws Exception {
        String resto = url.substring(url.indexOf("://") + 3);
        int barra = resto.indexOf('/');
        String hostPorta = barra < 0 ? resto : resto.substring(0, barra);
        String caminho = barra < 0 ? "/" : resto.substring(barra);
        String host = hostPorta; int porta = 80;
        int dp = hostPorta.indexOf(':');
        if (dp >= 0) { host = hostPorta.substring(0, dp); porta = Integer.parseInt(hostPorta.substring(dp + 1)); }
        try (Socket s = new Socket()) {
            s.connect(new InetSocketAddress(host, porta), 8000);
            s.setSoTimeout(url.matches(".*/(scan_mesh_node|wifi_list|nettb|c_upload|check_wan_type|add_mesh_node)(\\?.*)?$") || tipo.startsWith("multipart") ? 60000 : 15000);
            StringBuilder req = new StringBuilder();
            req.append(dados != null ? "POST " : "GET ").append(caminho).append(" HTTP/1.0\r\n");
            req.append("Host: ").append(host).append("\r\n");
            req.append("User-Agent: MiWiFiPainel-Android\r\nAccept: */*\r\nConnection: close\r\n");
            if (dados != null) {
                req.append("Content-Type: ").append(tipo).append("\r\n");
                req.append("Content-Length: ").append(dados.length).append("\r\n");
            }
            req.append("\r\n");
            OutputStream out = s.getOutputStream();
            out.write(req.toString().getBytes(StandardCharsets.ISO_8859_1));
            if (dados != null) out.write(dados);
            out.flush();
            InputStream in = s.getInputStream();
            ByteArrayOutputStream buf = new ByteArrayOutputStream();
            byte[] b = new byte[16384]; int n;
            while ((n = in.read(b)) > 0) buf.write(b, 0, n);
            byte[] tudo = buf.toByteArray();
            int fim = indexOf(tudo, "\r\n\r\n".getBytes(StandardCharsets.ISO_8859_1));
            String cab = new String(tudo, 0, fim < 0 ? tudo.length : fim, StandardCharsets.ISO_8859_1);
            byte[] corpo = fim < 0 ? new byte[0] : java.util.Arrays.copyOfRange(tudo, fim + 4, tudo.length);
            Resp r = new Resp();
            String[] linhas = cab.split("\r?\n");
            try { r.status = Integer.parseInt(linhas[0].split(" ")[1]); } catch (Exception e) { r.status = 0; }
            if (cab.toLowerCase().contains("transfer-encoding: chunked")) corpo = desfragmentar(corpo);
            r.corpo = new String(corpo, StandardCharsets.UTF_8);
            return r;
        }
    }

    private static int indexOf(byte[] a, byte[] alvo) {
        outer:
        for (int i = 0; i + alvo.length <= a.length; i++) {
            for (int j = 0; j < alvo.length; j++) if (a[i + j] != alvo[j]) continue outer;
            return i;
        }
        return -1;
    }

    private static byte[] desfragmentar(byte[] c) {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        int i = 0;
        try {
            while (i < c.length) {
                int fimLinha = i;
                while (fimLinha + 1 < c.length && !(c[fimLinha] == '\r' && c[fimLinha + 1] == '\n')) fimLinha++;
                String tam = new String(c, i, fimLinha - i, StandardCharsets.ISO_8859_1).split(";")[0].trim();
                int n = Integer.parseInt(tam, 16);
                if (n == 0) break;
                out.write(c, fimLinha + 2, n);
                i = fimLinha + 2 + n + 2;
            }
        } catch (Exception e) { return c; }
        return out.toByteArray();
    }

    private static String enc(String s) {
        try { return URLEncoder.encode(s, "UTF-8"); } catch (Exception e) { return s; }
    }

    private static String formulario(JSONObject p) {
        StringBuilder sb = new StringBuilder();
        if (p == null) return "";
        Iterator<String> it = p.keys();
        while (it.hasNext()) {
            String k = it.next();
            if (sb.length() > 0) sb.append('&');
            sb.append(enc(k)).append('=').append(enc(String.valueOf(p.opt(k))));
        }
        return sb.toString();
    }

    private static String sha1(String s) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA-1");
        byte[] d = md.digest(s.getBytes(StandardCharsets.UTF_8));
        StringBuilder sb = new StringBuilder();
        for (byte x : d) sb.append(String.format("%02x", x));
        return sb.toString();
    }

    private static String achar(Pattern p, String txt) {
        Matcher m = p.matcher(txt);
        return m.find() ? m.group(1) : null;
    }

    // ---------- funções do painel ----------
    private JSONObject login(String nome, String senha) throws Exception {
        String ip = roteadores.get(nome);
        String pagina = http("http://" + ip + "/cgi-bin/luci/web", null).corpo;
        String dev = achar(Pattern.compile("deviceId\\s*=\\s*'([^']+)'"), pagina);
        String chave = achar(Pattern.compile("key:\\s*'([0-9a-f]{32})'"), pagina);
        if (dev == null) dev = "";
        if (chave == null) chave = CHAVE_PADRAO;
        String nonce = "0_" + dev + "_" + (System.currentTimeMillis() / 1000) + "_" + new Random().nextInt(10000);
        String hash = sha1(nonce + sha1(senha + chave));
        String corpo = "username=admin&password=" + hash + "&logtype=2&nonce=" + enc(nonce);
        JSONObject j = new JSONObject(http("http://" + ip + "/cgi-bin/luci/api/xqsystem/login", corpo.getBytes(StandardCharsets.UTF_8)).corpo);
        JSONObject r = new JSONObject();
        if (j.optInt("code", -1) == 0 && j.optString("token", "").length() > 0) {
            sessoes.put(nome, j.getString("token"));
            cacheEndpoints.remove(nome);
            return r.put("ok", true);
        }
        return r.put("ok", false).put("erro", "Login recusado (code " + j.opt("code") + ")").put("resp", mascarar(j, false));
    }

    private static Object mascarar(Object o, boolean mostrar) throws Exception {
        if (mostrar) return o;
        if (o instanceof JSONObject) {
            JSONObject j = (JSONObject) o, n = new JSONObject();
            Iterator<String> it = j.keys();
            while (it.hasNext()) {
                String k = it.next(); Object v = j.get(k);
                boolean simples = v instanceof String || v instanceof Number;
                if (SENSIVEIS.matcher(k).find() && simples && !"".equals(v)) n.put(k, "••••••");
                else n.put(k, mascarar(v, false));
            }
            return n;
        }
        if (o instanceof JSONArray) {
            JSONArray a = (JSONArray) o, n = new JSONArray();
            for (int i = 0; i < a.length(); i++) n.put(mascarar(a.get(i), false));
            return n;
        }
        return o;
    }

    private JSONObject chamar(String nome, String endpoint, String metodo, JSONObject params, boolean mostrar) throws Exception { return chamar(nome, endpoint, metodo, params, mostrar, null); }

    private JSONObject chamar(String nome, String endpoint, String metodo, JSONObject params, boolean mostrar, JSONObject arquivo) throws Exception {
        JSONObject r = new JSONObject();
        String token = sessoes.get(nome);
        if (token == null) return r.put("ok", false).put("erro", "Faça login neste roteador primeiro.");
        String ep = endpoint.replaceAll("^/+", "");
        if (!ep.startsWith("api/")) ep = "api/" + ep;
        String url = "http://" + roteadores.get(nome) + "/cgi-bin/luci/;stok=" + token + "/" + ep;
        byte[] dados = null;
        String f = formulario(params);
        if ("POST".equals(metodo)) dados = (f.isEmpty() ? " " : f).getBytes(StandardCharsets.UTF_8);
        else if (!f.isEmpty()) url += "?" + f;
        String tipo = "application/x-www-form-urlencoded";
        if (arquivo != null) { Object[] m = multipart(params, arquivo); dados = (byte[]) m[0]; tipo = (String) m[1]; }
        Resp resp;
        try { resp = http(url, dados, tipo); } catch (Exception e) { return r.put("ok", false).put("erro", String.valueOf(e.getMessage())); }
        String txt = resp.corpo.trim();
        try {
            Object corpo = txt.startsWith("[") ? new JSONArray(txt) : new JSONObject(txt);
            if (corpo instanceof JSONObject && ((JSONObject) corpo).optInt("code", 0) == 401) {
                sessoes.remove(nome);
                return r.put("ok", false).put("erro", "Sessão expirada: faça login de novo.").put("status", resp.status);
            }
            return r.put("ok", true).put("status", resp.status).put("json", mascarar(corpo, mostrar));
        } catch (Exception e) {
            return r.put("ok", true).put("status", resp.status).put("texto", txt.length() > 3000 ? txt.substring(0, 3000) : txt);
        }
    }

    private JSONArray descobrir(String nome) {
        JSONArray cache = cacheEndpoints.get(nome);
        if (cache != null) return cache;
        String token = sessoes.get(nome);
        if (token == null) return new JSONArray();
        String ip = roteadores.get(nome);
        TreeSet<String> achados = new TreeSet<>();
        Collections.addAll(achados, EXTRAS);
        for (String p : PAGINAS) {
            String html;
            try { html = http("http://" + ip + "/cgi-bin/luci/;stok=" + token + "/" + p, null).corpo; } catch (Exception e) { continue; }
            Matcher m = API_RE.matcher(html);
            while (m.find()) achados.add(m.group());
            Matcher s = SRC_RE.matcher(html);
            while (s.find()) {
                String src = s.group(1);
                if (src.startsWith("/")) src = "http://" + ip + src;
                else if (!src.startsWith("http")) continue;
                try {
                    Matcher mj = API_RE.matcher(http(src, null).corpo);
                    while (mj.find()) achados.add(mj.group());
                } catch (Exception ignored) { }
            }
        }
        List<String[]> lista = new ArrayList<>();
        for (String e : achados) {
            String ult = e.contains("/") ? e.substring(e.indexOf('/', e.indexOf('/') + 1) + 1) : e;
            lista.add(new String[]{e, ESCRITA.matcher(ult).find() ? "1" : "0"});
        }
        Collections.sort(lista, new java.util.Comparator<String[]>() {
            @Override public int compare(String[] a, String[] b) { return a[1].equals(b[1]) ? a[0].compareTo(b[0]) : a[1].compareTo(b[1]); }
        });
        JSONArray out = new JSONArray();
        try { for (String[] x : lista) out.put(new JSONObject().put("endpoint", x[0]).put("escrita", "1".equals(x[1]))); } catch (Exception ignored) { }
        cacheEndpoints.put(nome, out);
        return out;
    }

    private JSONObject despejar(String nome) throws Exception {
        JSONObject r = new JSONObject();
        String token = sessoes.get(nome);
        if (token == null) return r.put("ok", false).put("erro", "Faça login primeiro.");
        String ip = roteadores.get(nome);
        File pasta = new File(ctx.getExternalFilesDir(null), "dump/" + nome);
        pasta.mkdirs();
        TreeSet<String> paginas = new TreeSet<>();
        Collections.addAll(paginas, PAGINAS);
        try {
            String home = http("http://" + ip + "/cgi-bin/luci/;stok=" + token + "/web/home", null).corpo.replace(token, "");
            Matcher m = Pattern.compile("/(web/[a-z_/]+)").matcher(home);
            while (m.find()) paginas.add(m.group(1));
            paginas.remove("web/logout"); paginas.remove("web/login");  // buscar 'logout' encerra a sessão
        } catch (Exception ignored) { }
        JSONArray salvos = new JSONArray();
        for (String p : paginas) {
            Resp resp;
            try { resp = http("http://" + ip + "/cgi-bin/luci/;stok=" + token + "/" + p, null); } catch (Exception e) { continue; }
            if (resp.status != 200) continue;
            try (FileOutputStream f = new FileOutputStream(new File(pasta, p.replace('/', '_') + ".html"))) {
                f.write(resp.corpo.replace(token, "TOKEN").getBytes(StandardCharsets.UTF_8));
            }
            salvos.put(p);
        }
        return r.put("ok", true).put("paginas", salvos).put("pasta", pasta.getAbsolutePath());
    }

    // ---------- servidor HTTP local ----------
    public synchronized void iniciar() throws Exception {
        if (servidor != null) return;
        servidor = new ServerSocket();
        servidor.setReuseAddress(true);
        servidor.bind(new InetSocketAddress(InetAddress.getByName("127.0.0.1"), PORTA));
        final ServerSocket ss = servidor;
        Thread t = new Thread(new Runnable() {
            @Override public void run() {
                while (!ss.isClosed()) {
                    try {
                        final Socket c = ss.accept();
                        pool.execute(new Runnable() { @Override public void run() { atender(c); } });
                    } catch (Exception ignored) { }
                }
            }
        }, "miwifi-servidor");
        t.setDaemon(true);
        t.start();
    }

    public synchronized void parar() {
        try { if (servidor != null) servidor.close(); } catch (Exception ignored) { }
        servidor = null;
    }

    private static String lerLinha(InputStream in) throws Exception {
        ByteArrayOutputStream b = new ByteArrayOutputStream();
        int c;
        while ((c = in.read()) >= 0) {
            if (c == '\n') break;
            if (c != '\r') b.write(c);
        }
        return b.toString("UTF-8");
    }

    private void atender(Socket c) {
        try (Socket s = c) {
            s.setSoTimeout(30000);
            InputStream in = s.getInputStream();
            String primeira = lerLinha(in);
            if (primeira.isEmpty()) return;
            String[] partes = primeira.split(" ");
            String metodo = partes[0], alvo = partes.length > 1 ? partes[1] : "/";
            int tam = 0; String l;
            while (!(l = lerLinha(in)).isEmpty()) {
                if (l.toLowerCase().startsWith("content-length:")) tam = Integer.parseInt(l.substring(15).trim());
            }
            byte[] corpo = new byte[tam]; int lidos = 0;
            while (lidos < tam) { int n = in.read(corpo, lidos, tam - lidos); if (n < 0) break; lidos += n; }
            String caminho = alvo.contains("?") ? alvo.substring(0, alvo.indexOf('?')) : alvo;
            String consulta = alvo.contains("?") ? alvo.substring(alvo.indexOf('?') + 1) : "";
            OutputStream out = s.getOutputStream();
            if ("GET".equals(metodo)) responderGet(out, caminho, consulta);
            else responderPost(out, caminho, new String(corpo, StandardCharsets.UTF_8));
        } catch (Exception ignored) { }
    }

    private static void enviar(OutputStream out, int codigo, String tipo, byte[] dados) throws Exception {
        String cab = "HTTP/1.1 " + codigo + (codigo == 200 ? " OK" : " Erro") + "\r\nContent-Type: " + tipo
            + "\r\nContent-Length: " + dados.length + "\r\nCache-Control: no-store\r\nConnection: close\r\n\r\n";
        out.write(cab.getBytes(StandardCharsets.ISO_8859_1));
        out.write(dados);
        out.flush();
    }

    private static void json(OutputStream out, int codigo, Object o) throws Exception {
        enviar(out, codigo, "application/json; charset=utf-8", o.toString().getBytes(StandardCharsets.UTF_8));
    }

    private void responderGet(OutputStream out, String caminho, String consulta) throws Exception {
        if ("/".equals(caminho)) {
            InputStream a = ctx.getAssets().open("painel.html");
            ByteArrayOutputStream b = new ByteArrayOutputStream();
            byte[] x = new byte[16384]; int n;
            while ((n = a.read(x)) > 0) b.write(x, 0, n);
            a.close();
            String html = b.toString("UTF-8").replaceFirst("<head>",
                "<head><script>window.__MIWIFI_RODAPE__='Painel no celular · fala direto com os roteadores na rede de casa · alterações sempre pedem confirmação · <span class=\"oculto\">oculto</span> = função que não aparece na interface original';</script>");
            enviar(out, 200, "text/html; charset=utf-8", html.getBytes(StandardCharsets.UTF_8));
        } else if ("/api/estado".equals(caminho)) {
            JSONObject logado = new JSONObject();
            synchronized (roteadores) { for (String k : roteadores.keySet()) logado.put(k, sessoes.containsKey(k)); }
            json(out, 200, new JSONObject().put("roteadores", new JSONObject(new LinkedHashMap<>(roteadores))).put("logado", logado));
        } else if ("/api/endpoints".equals(caminho)) {
            String nome = "";
            for (String par : consulta.split("&")) if (par.startsWith("roteador=")) nome = java.net.URLDecoder.decode(par.substring(9), "UTF-8");
            json(out, 200, descobrir(nome));
        } else {
            json(out, 404, new JSONObject().put("erro", "não encontrado"));
        }
    }

    private void responderPost(OutputStream out, String caminho, String txt) throws Exception {
        JSONObject corpo = txt.trim().isEmpty() ? new JSONObject() : new JSONObject(txt);
        if ("/api/sair".equals(caminho)) {
            json(out, 200, new JSONObject().put("ok", true));
            if (aoSair != null) aoSair.run();
            return;
        }
        if ("/api/config".equals(caminho)) {
            LinkedHashMap<String, String> novos = new LinkedHashMap<>();
            JSONArray lst = corpo.optJSONArray("roteadores");
            for (int i = 0; lst != null && i < lst.length(); i++) {
                JSONObject it = lst.getJSONObject(i);
                String n = it.optString("nome", "").trim().toLowerCase().replaceAll("[^a-z0-9_-]", "");
                if (n.length() > 30) n = n.substring(0, 30);
                String ip = it.optString("ip", "").trim();
                if (n.isEmpty() || !IP_RE.matcher(ip).matches()) {
                    json(out, 400, new JSONObject().put("ok", false).put("erro", "Nome ou IP inválido: " + it)); return;
                }
                novos.put(n, ip);
            }
            if (novos.isEmpty()) { json(out, 400, new JSONObject().put("ok", false).put("erro", "Informe pelo menos um roteador.")); return; }
            for (String n : new ArrayList<>(sessoes.keySet())) if (!java.util.Objects.equals(novos.get(n), roteadores.get(n))) sessoes.remove(n);  // IP mudou: sessão antiga não vale
            roteadores.clear(); roteadores.putAll(novos); cacheEndpoints.clear(); salvarCfg();
            json(out, 200, new JSONObject().put("ok", true).put("roteadores", new JSONObject(novos)));
            return;
        }
        String nome = corpo.optString("roteador", null);
        if (nome == null || !roteadores.containsKey(nome)) { json(out, 400, new JSONObject().put("ok", false).put("erro", "roteador inválido")); return; }
        switch (caminho) {
            case "/api/login":
                try { json(out, 200, login(nome, corpo.optString("senha", ""))); }
                catch (Exception e) { json(out, 200, new JSONObject().put("ok", false).put("erro", String.valueOf(e.getMessage()))); }
                return;
            case "/api/despejar":
                json(out, 200, despejar(nome)); return;
            case "/api/logout":
                sessoes.remove(nome); json(out, 200, new JSONObject().put("ok", true)); return;
            case "/api/chamar": {
                String ep = corpo.optString("endpoint", "");
                String ult = ep.contains("/") ? ep.substring(ep.lastIndexOf('/') + 1) : ep;
                String metodo = corpo.optString("metodo", "GET");
                JSONObject arquivo = corpo.optJSONObject("arquivo");
                boolean escrita = ESCRITA.matcher(ult).find() || "POST".equals(metodo) || arquivo != null;
                if (escrita && !corpo.optBoolean("confirmado", false)) {
                    json(out, 200, new JSONObject().put("ok", false).put("erro", "Este endpoint altera o roteador: confirme antes.")); return;
                }
                json(out, 200, chamar(nome, ep, metodo, corpo.optJSONObject("params"), corpo.optBoolean("mostrar", false), arquivo));
                return;
            }
            default:
                json(out, 404, new JSONObject().put("erro", "não encontrado"));
        }
    }
}
