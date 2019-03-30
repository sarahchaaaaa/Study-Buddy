package com.example.studybuddy_android;

import android.support.v7.app.AppCompatActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //Button logInButton = (Button) findViewById(R.id.logInButton);
        /*
        logInButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                setContentView(R.layout.);
            }
        });
        */

        Button createProfButton = (Button) findViewById(R.id.createProfileButton);
        createProfButton.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent homeIntent = new Intent(MainActivity.this, NewProfileActivity.class);
                startActivity(homeIntent);
            }
        });
    }
}
