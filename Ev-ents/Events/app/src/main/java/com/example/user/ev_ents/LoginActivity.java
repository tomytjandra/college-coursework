package com.example.user.ev_ents;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import Controller.UsersController;

public class LoginActivity extends AppCompatActivity {

    final UsersController users = UsersController.getInstance();
    Button btnLogin;
    EditText txtUsername, txtPassword;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        btnLogin = findViewById(R.id.btnLogin);
        txtUsername = findViewById(R.id.txtUsernameLogin);
        txtPassword = findViewById(R.id.txtPasswordLogin);

        btnLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                boolean flag = true;
                String username = txtUsername.getText().toString();
                String password = txtPassword.getText().toString();

                if (username.equals("")) {
                    txtUsername.setError("Username must be filled");
                    flag = false;
                }
                if (password.equals("")) {
                    txtPassword.setError("Password must be filled");
                    flag = false;
                }

                if (flag) {
                    if (users.searchUserID(username,password).equals("")) {
                        Toast.makeText(LoginActivity.this, "Wrong username or password", Toast.LENGTH_SHORT).show();
                    }else {
                        Toast.makeText(LoginActivity.this, "Login Successful", Toast.LENGTH_SHORT).show();
                        finish();
                        Intent intentHomepage = new Intent(getApplicationContext(),HomeActivity.class);
                        intentHomepage.putExtra("CurrentUserID", users.searchUserID(username,password));
                        startActivity(intentHomepage);
                    }
                }
            }
        });
    }
}
