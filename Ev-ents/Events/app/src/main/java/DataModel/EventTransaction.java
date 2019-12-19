package DataModel;

import java.util.Date;

/**
 * Created by USER on 3/3/2018.
 */

public class EventTransaction {
    private String transactionID;
    private String userID;
    private String eventID;
    private int qty;
    private Date transactionDate;

    public EventTransaction(String transactionID, String userID, String eventID, int qty, Date transactionDate) {
        this.transactionID = transactionID;
        this.userID = userID;
        this.eventID = eventID;
        this.qty = qty;
        this.transactionDate = transactionDate;
    }

    public String getTransactionID() {
        return transactionID;
    }

    public String getUserID() {
        return userID;
    }

    public String getEventID() {
        return eventID;
    }

    public int getQty() {
        return qty;
    }

    public Date getTransactionDate() {
        return transactionDate;
    }
}
