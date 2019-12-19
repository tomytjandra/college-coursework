package Controller;

import java.util.ArrayList;

import DataModel.EventTransaction;

/**
 * Created by USER on 3/10/2018.
 */

public class EventTransactionController {
    private ArrayList<EventTransaction> listEventTransaction;
    private static EventTransactionController instance;

    public EventTransactionController() {
        listEventTransaction = new ArrayList<EventTransaction>();
    }

    public static EventTransactionController getInstance() {
        if (instance == null) {
            instance = new EventTransactionController();
        }
        return instance;
    }

    public ArrayList<EventTransaction> getListEventTransaction() {
        return listEventTransaction;
    }

    public void addEventTransaction(EventTransaction eventTransaction) {
        listEventTransaction.add(eventTransaction);
    }

    public ArrayList<EventTransaction> getPurchasedEventList(String userID) {
        ArrayList<EventTransaction> purchasedEventList = new ArrayList<EventTransaction>();

        for (int i = 0; i < this.listEventTransaction.size() ; i++) {
            if (listEventTransaction.get(i).getUserID().equals(userID)) {
                purchasedEventList.add(listEventTransaction.get(i));
            }
        }

        return purchasedEventList;
    }

}
