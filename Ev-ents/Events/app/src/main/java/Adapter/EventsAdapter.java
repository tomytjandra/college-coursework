package Adapter;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import com.example.user.ev_ents.R;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;

import DataModel.Events;

/**
 * Created by USER on 3/25/2018.
 */

public class EventsAdapter extends BaseAdapter {

    private ArrayList<Events> listEvents;

    public EventsAdapter(ArrayList<Events> listEvents) {
        this.listEvents = listEvents;
    }

    @Override
    public int getCount() {
        return listEvents.size();
    }

    @Override
    public Events getItem(int i) {
        return listEvents.get(i);
    }

    @Override
    public long getItemId(int i) {
        return 0;
    }

    @Override
    public View getView(int i, View view, ViewGroup viewGroup) {
        LayoutInflater inflater = LayoutInflater.from(viewGroup.getContext());
        view = inflater.inflate(R.layout.list_view_event,null);

        TextView lblEventID = view.findViewById(R.id.lblEventID);
        TextView lblEventName = view.findViewById(R.id.lblEventName);
        TextView lblStartDate = view.findViewById(R.id.lblStartDate);
        TextView lblEndDate = view.findViewById(R.id.lblEndDate);
        TextView lblRating = view.findViewById(R.id.lblRating);

        lblEventID.setText(getItem(i).getEventID());
        lblEventName.setText(getItem(i).getEventName());

        DateFormat dateFormatter = new SimpleDateFormat("E, dd MMM yyyy");
        lblStartDate.setText("Start: "+dateFormatter.format(getItem(i).getStartDate()));
        lblEndDate.setText("End: "+dateFormatter.format(getItem(i).getEndDate()));
        lblRating.setText("Rating: "+getItem(i).getRating());

        return view;
    }
}
