package com.wmariz.miwifipainel;

import android.app.Activity;
import android.app.AlertDialog;
import android.graphics.Color;
import android.os.Bundle;
import android.view.Window;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

/** Single screen: shows the panel (the same HTML as the PC panel) served by the local Servidor. */
public class MainActivity extends Activity {
    private static Servidor servidor;  // one per process: survives screen rotation
    private WebView web;

    @Override
    protected void onCreate(Bundle estado) {
        super.onCreate(estado);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setStatusBarColor(Color.parseColor("#ff6900"));
        web = new WebView(this);
        setContentView(web);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setUseWideViewPort(true);
        s.setLoadWithOverviewMode(true);
        s.setBuiltInZoomControls(true);
        s.setDisplayZoomControls(false);
        web.setWebChromeClient(new WebChromeClient());  // needed for the panel's confirm()/alert()
        web.setWebViewClient(new WebViewClient());
        try {
            if (servidor == null) {
                servidor = new Servidor(getApplicationContext(), new Runnable() {
                    @Override public void run() {
                        runOnUiThread(new Runnable() { @Override public void run() { finishAndRemoveTask(); } });
                    }
                });
                servidor.iniciar();
            }
        } catch (Exception e) {
            new AlertDialog.Builder(this).setTitle("MiWiFi Painel")
                .setMessage("Não foi possível iniciar o painel: " + e.getMessage())
                .setPositiveButton("OK", new android.content.DialogInterface.OnClickListener() {
                    @Override public void onClick(android.content.DialogInterface d, int w) { finish(); }
                }).show();
            return;
        }
        if (estado != null) web.restoreState(estado);
        else web.loadUrl("http://127.0.0.1:" + Servidor.PORTA + "/");
    }

    @Override
    protected void onSaveInstanceState(Bundle out) {
        super.onSaveInstanceState(out);
        if (web != null) web.saveState(out);
    }

    @Override
    public void onBackPressed() {
        if (web != null && web.canGoBack()) web.goBack();
        else super.onBackPressed();
    }

    @Override
    protected void onDestroy() {
        if (isFinishing() && servidor != null) { servidor.parar(); servidor = null; }
        super.onDestroy();
    }
}
