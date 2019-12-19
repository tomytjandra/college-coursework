package com.example.user.ev_ents;

import android.content.DialogInterface;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.util.Date;

import Controller.EventTransactionController;
import Controller.EventsController;
import Controller.UsersController;
import DataModel.EventTransaction;

public class BuyFormActivity extends AppCompatActivity {

    final EventsController events = EventsController.getInstance();
    final UsersController users = UsersController.getInstance();
    final EventTransactionController eventTransaction = EventTransactionController.getInstance();

    EditText txtEventID, txtQuantity;
    Button btnBuyTicket;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_buy_form);

        txtEventID = findViewById(R.id.txtEventID);
        txtQuantity = findViewById(R.id.txtQuantity);
        btnBuyTicket = findViewById(R.id.btnBuyTicket);

        btnBuyTicket.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                boolean flag = true;
                String eventID = txtEventID.getText().toString();
                int quantity = 0;
                if(txtQuantity.getText().length() > 0){
                    quantity = Integer.parseInt(txtQuantity.getText().toString());
                }

                if(eventID.equals("")){
                    txtEventID.setError("EventID must be filled");
                    flag = false;
                }else if(!events.isEventRegistered(eventID)){
                    txtEventID.setError("EventID must exists");
                    flag = false;
                }

                if(txtQuantity.getText().equals("")) {
                    txtQuantity.setError("Quantity must be filled");
                    flag = false;
                }else if(quantity < 1){
                    txtQuantity.setError("Quantity must not less than 1");
                    flag = false;
                }

                if(flag) {
                    String userID = users.getCurrentUserID();
                    String transactionID = "ET"+String.format("%03d", eventTransaction.getListEventTransaction().size()+1);

                    eventTransaction.addEventTransaction(new EventTransaction(transactionID, userID, eventID, quantity, new Date()));
                    Toast.makeText(BuyFormActivity.this, "Buy Success", Toast.LENGTH_SHORT).show();
                    txtEventID.setText("");
                    txtQuantity.setText("");
                }
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.menu_home,menu);

        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if (id == R.id.itemHomePage) {
            finish();
            Intent intentHomepage = new Intent(getApplicationContext(),HomeActivity.class);
            startActivity(intentHomepage);
        } else if (id == R.id.itemViewAllEvents) {
            finish();
            Intent intentViewAllEvents = new Intent(getApplicationContext(),ViewAllEventActivity.class);
            startActivity(intentViewAllEvents);
        } else if (id == R.id.itemBuyForm) {
            finish();
            Intent intentBuyForm = new Intent(getApplicationContext(),BuyFormActivity.class);
            startActivity(intentBuyForm);
        } else if (id == R.id.itemLogout) {
            triggerAlertDialogLogout();
        }

        return super.onOptionsItemSelected(item);
    }

    public void onBackPressed() {
        triggerAlertDialogLogout();
    }

    public void triggerAlertDialogLogout() {
        AlertDialog.Builder builderLogout;

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            builderLogout = new AlertDialog.Builder(this, android.R.style.Theme_Material_Dialog_Alert);
        } else {
            builderLogout = new AlertDialog.Builder(this);
        }

        builderLogout.setTitle("Logout");
        builderLogout.setMessage("Do you want to logout?");
        builderLogout.setCancelable(true);
        builderLogout.setIcon(android.R.drawable.ic_dialog_alert);

        builderLogout.setPositiveButton(
                "Yes",
                new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        finish();
                    }
                }
        );

        builderLogout.setNegativeButton(
                "No",
                new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        dialogInterface.cancel();
                    }
                }
        );

        AlertDialog dialogLogout = builderLogout.create();
        dialogLogout.show();
    }
}
