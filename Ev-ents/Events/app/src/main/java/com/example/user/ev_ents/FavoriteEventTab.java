package com.example.user.ev_ents;

import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;

import java.util.ArrayList;

import Adapter.EventsAdapter;
import Controller.EventsController;
import DataModel.Events;

/**
 * Created by USER on 3/10/2018.
 */

public class FavoriteEventTab extends Fragment {

    ArrayList<Events> listTop3Events;
    ListView listViewFavoriteEvent;
    EventsAdapter eventsAdapter;

    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.tab_favorite_event, container, false);

        listTop3Events = EventsController.getInstance().getTop3Events();

        listViewFavoriteEvent = rootView.findViewById(R.id.listViewFavoriteEvent);
        eventsAdapter = new EventsAdapter(listTop3Events);
        listViewFavoriteEvent.setAdapter(eventsAdapter);

        return rootView;
    }

}
