package DataModel;

import java.util.Date;

/**
 * Created by USER on 3/3/2018.
 */

public class Events {
    private String eventID;
    private String eventName;
    private String description;
    private String location;
    private Date startDate;
    private Date endDate;
    private int rating;
    private double latitude;
    private double longitude;

    public Events(String eventID, String eventName, String description, String location, Date startDate, Date endDate, int rating, double latitude, double longitude) {
        this.eventID = eventID;
        this.eventName = eventName;
        this.description = description;
        this.location = location;
        this.startDate = startDate;
        this.endDate = endDate;
        this.rating = rating;
        this.latitude = latitude;
        this.longitude = longitude;
    }

    public String getEventID() {
        return eventID;
    }

    public String getEventName() {
        return eventName;
    }

    public String getDescription() {
        return description;
    }

    public String getLocation() {
        return location;
    }

    public Date getStartDate() {
        return startDate;
    }

    public Date getEndDate() {
        return endDate;
    }

    public int getRating() {
        return rating;
    }

    public double getLatitude() {
        return latitude;
    }

    public double getLongitude() {
        return longitude;
    }
}
