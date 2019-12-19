package com.example.user.ev_ents;

import android.content.DialogInterface;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import Controller.UsersController;
import DataModel.Users;

public class MainActivity extends AppCompatActivity {

    final UsersController users = UsersController.getInstance();
    Button btnLoginActivity, btnRegisterActivity;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        btnLoginActivity = findViewById(R.id.btnLoginActivity);
        btnRegisterActivity = findViewById(R.id.btnRegisterActivity);
        users.setCurrentUserID("");

        btnLoginActivity.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intentLogin = new Intent(getApplicationContext(),LoginActivity.class);
                startActivity(intentLogin);
            }
        });

        btnRegisterActivity.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intentRegister = new Intent(getApplicationContext(),RegisterActivity.class);
                startActivity(intentRegister);
            }
        });

        /*
        //generate data dummy
        btnRegisterActivity.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View view) {
                String temp = String.format("%03d", users.getListUsers().size()+1);
                String userID = "US"+temp;
                users.addUser(
                        new Users(userID,
                                "Tomy "+temp,
                                "tomy"+temp,
                                "tomy"+temp,
                                "Male",
                                "123456789"+temp,
                                "Jl. Binus "+temp));
                Toast.makeText(MainActivity.this, userID+" created", Toast.LENGTH_SHORT).show();
                return false;
            }
        });
        */
    }

    public void onBackPressed() {
        AlertDialog.Builder builderExit;

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            builderExit = new AlertDialog.Builder(this, android.R.style.Theme_Material_Dialog_Alert);
        } else {
            builderExit = new AlertDialog.Builder(this);
        }

        builderExit.setTitle("Exit Application");
        builderExit.setMessage("Do you want to exit?");
        builderExit.setCancelable(true);
        builderExit.setIcon(android.R.drawable.ic_dialog_alert);

        builderExit.setPositiveButton(
                "Yes",
                new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        finish();
                    }
                }
        );

        builderExit.setNegativeButton(
                "No",
                new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        dialogInterface.cancel();
                    }
                }
        );

        AlertDialog dialogExit = builderExit.create();
        dialogExit.show();
    }
}
