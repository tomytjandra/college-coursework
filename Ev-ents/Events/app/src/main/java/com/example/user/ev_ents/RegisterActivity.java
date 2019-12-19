package com.example.user.ev_ents;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.Toast;

import Controller.UsersController;
import DataModel.Users;

public class RegisterActivity extends AppCompatActivity {

    final UsersController users = UsersController.getInstance();
    EditText txtFullname, txtUsername, txtPassword, txtPhoneNumber, txtAddress;
    RadioButton rbMale, rbFemale;
    Button btnRegister;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        txtFullname = findViewById(R.id.txtFullname);
        txtUsername = findViewById(R.id.txtUsername);
        txtPassword = findViewById(R.id.txtPassword);
        rbMale = findViewById(R.id.rbMale);
        rbFemale = findViewById(R.id.rbFemale);
        txtPhoneNumber = findViewById(R.id.txtPhoneNumber);
        txtAddress = findViewById(R.id.txtAddress);
        btnRegister = findViewById(R.id.btnRegister);

        btnRegister.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                boolean flag = true;
                String fullname = txtFullname.getText().toString();
                String username = txtUsername.getText().toString();
                String password = txtPassword.getText().toString();
                boolean isMale = rbMale.isChecked();
                boolean isFemale = rbFemale.isChecked();
                String phoneNumber = txtPhoneNumber.getText().toString();
                String address = txtAddress.getText().toString();

                if (fullname.equals("")) {
                    txtFullname.setError("Full Name must be filled");
                    flag = false;
                }
                if (username.equals("")) {
                    txtUsername.setError("Username must be filled");
                    flag = false;
                }else if (username.length()<5 || username.length()>30) {
                    txtUsername.setError("Username length must be between 5 and 30 characters");
                    flag = false;
                }

                if(password.equals("")) {
                    txtPassword.setError("Password must be filled");
                    flag = false;
                }else if(password.length()<5) {
                    txtPassword.setError("Password length must be at least 5 characters");
                    flag = false;
                }else if(!checkPasswordFormat(password)) {
                    txtPassword.setError("Password must contains at least 1 character and 1 numeric");
                    flag = false;
                }

                if(!isMale && !isFemale) {
                    Toast.makeText(RegisterActivity.this, "Gender must be chosen", Toast.LENGTH_SHORT).show();
                    flag = false;
                }

                if(!checkPhoneNumberFormat(phoneNumber)) {
                    txtPhoneNumber.setError("Phone Number must be numeric");
                    flag = false;
                }else if(phoneNumber.length()<8 || phoneNumber.length()>20) {
                    txtPhoneNumber.setError("Phone Number length must be between 8 and 20 digits");
                    flag = false;
                }

                if(address.equals("")) {
                    txtAddress.setError("Address must be filled");
                    flag = false;
                }

                if(flag) {
                    if(users.isUsernameRegistered(username)) {
                        Toast.makeText(RegisterActivity.this, username+" is already registered", Toast.LENGTH_SHORT).show();
                    }else {
                        String userID = "US"+String.format("%03d", users.getListUsers().size()+1);
                        String gender = "";
                        if(isMale){
                            gender = "Male";
                        }else if(isFemale){
                            gender = "Female";
                        }

                        users.addUser(new Users(userID,fullname,username,password,gender,phoneNumber,address));
                        Toast.makeText(RegisterActivity.this, "Register "+username+" Success", Toast.LENGTH_SHORT).show();
                        finish();
                        Intent intentHomepage = new Intent(getApplicationContext(),HomeActivity.class);
                        intentHomepage.putExtra("CurrentUserID", userID);
                        startActivity(intentHomepage);
                    }
                }
            }
        });
    }

    public boolean checkPasswordFormat(String password){
        boolean flag = false;
        int countLower = 0, countUpper = 0, countNumeric = 0;

        for (int i = 0; i < password.length(); i++){
            char c = password.charAt(i);
            if(c >= 'a' && c <= 'z'){
                countLower++;
            }else if(c >= 'A' && c <= 'Z'){
                countUpper++;
            }else if(c >= '0' && c <= '9'){
                countNumeric++;
            }
        }

        if((countLower >= 1 || countUpper >= 1) && countNumeric >= 1){
            flag = true;
        }

        return flag;
    }

    public boolean checkPhoneNumberFormat(String phoneNumber){
        boolean flag = true;

        for (int i = 0; i < phoneNumber.length(); i++){
            char c = phoneNumber.charAt(i);
            if(c < '0' || c > '9'){
                flag = false;
                break;
            }
        }

        return flag;
    }
}
