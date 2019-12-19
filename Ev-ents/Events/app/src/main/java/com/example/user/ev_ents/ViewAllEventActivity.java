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
import android.widget.ListView;

import java.util.ArrayList;

import Adapter.EventsAdapter;
import Controller.EventsController;
import DataModel.Events;

public class ViewAllEventActivity extends AppCompatActivity {

    ArrayList<Events> listEvents;
    ListView listViewAllEvent;
    EventsAdapter eventsAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_all_event);

        listEvents = EventsController.getInstance().getListEvents();

        listViewAllEvent = findViewById(R.id.listViewAllEvent);
        eventsAdapter = new EventsAdapter(listEvents);
        listViewAllEvent.setAdapter(eventsAdapter);
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
