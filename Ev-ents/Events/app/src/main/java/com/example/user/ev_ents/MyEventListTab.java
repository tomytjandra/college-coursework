package com.example.user.ev_ents;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;
import android.widget.TextView;

import java.util.ArrayList;

import Adapter.EventTransactionAdapter;
import Controller.EventTransactionController;
import Controller.UsersController;
import DataModel.EventTransaction;

/**
 * Created by USER on 3/10/2018.
 */

public class MyEventListTab extends Fragment {

    ArrayList<EventTransaction> purchasedEventList;
    String currentUserID;
    ListView listViewMyEventList;
    EventTransactionAdapter eventTransactionAdapter;
    TextView lblNoData;

    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.tab_my_event_list, container, false);

        currentUserID = UsersController.getInstance().getCurrentUserID();
        purchasedEventList = EventTransactionController.getInstance().getPurchasedEventList(currentUserID);

        listViewMyEventList = rootView.findViewById(R.id.listViewMyEventList);
        eventTransactionAdapter = new EventTransactionAdapter(purchasedEventList);
        lblNoData = rootView.findViewById(R.id.lblNoData);

        if (purchasedEventList.size() == 0) {
            lblNoData.setText("No Purchased Event");
        } else {
            lblNoData.setText("");
            listViewMyEventList.setAdapter(eventTransactionAdapter);
        }

        return rootView;
    }
}
