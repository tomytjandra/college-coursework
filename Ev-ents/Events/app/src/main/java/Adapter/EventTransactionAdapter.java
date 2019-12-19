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

import Controller.EventsController;
import DataModel.EventTransaction;
import DataModel.Events;

/**
 * Created by USER on 3/27/2018.
 */

public class EventTransactionAdapter extends BaseAdapter{

    private ArrayList<EventTransaction> listEventTransaction;

    public EventTransactionAdapter(ArrayList<EventTransaction> listEventTransaction) {
        this.listEventTransaction = listEventTransaction;
    }

    @Override
    public int getCount() {
        return listEventTransaction.size();
    }

    @Override
    public EventTransaction getItem(int i) {
        return listEventTransaction.get(i);
    }

    @Override
    public long getItemId(int i) {
        return 0;
    }

    @Override
    public View getView(int i, View view, ViewGroup viewGroup) {
        LayoutInflater inflater = LayoutInflater.from(viewGroup.getContext());
        view = inflater.inflate(R.layout.list_view_purchased_event,null);

        TextView lblEventID = view.findViewById(R.id.lblEventID);
        TextView lblEventName = view.findViewById(R.id.lblEventName);
        TextView lblStartDate = view.findViewById(R.id.lblStartDate);
        TextView lblEndDate = view.findViewById(R.id.lblEndDate);
        TextView lblTransactionDate = view.findViewById(R.id.lblTransactionDate);
        TextView lblQuantity = view.findViewById(R.id.lblQuantity);

        String eventID = getItem(i).getEventID();
        Events event = EventsController.getInstance().getOneEvent(eventID);

        lblEventID.setText(eventID);
        lblEventName.setText(event.getEventName());

        DateFormat dateFormatter = new SimpleDateFormat("E, dd MMM yyyy");
        lblStartDate.setText("Start: "+dateFormatter.format(event.getStartDate()));
        lblEndDate.setText("End: "+dateFormatter.format(event.getEndDate()));

        DateFormat transactionDateFormatter = new SimpleDateFormat("E, dd MMM yyyy [HH:mm:ss]");
        lblTransactionDate.setText("Purchased: "+transactionDateFormatter.format(getItem(i).getTransactionDate()));
        lblQuantity.setText("Quantity: "+getItem(i).getQty());

        return view;
    }

}
