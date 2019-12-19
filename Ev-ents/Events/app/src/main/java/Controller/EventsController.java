package Controller;

import android.annotation.SuppressLint;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;

import DataModel.Events;

/**
 * Created by USER on 3/10/2018.
 */

public class EventsController {
    private ArrayList<Events> listEvents;
    private static EventsController instance;

    public EventsController() {
        listEvents = new ArrayList<Events>();
        try {
            initializeEvents();
        } catch (ParseException e) {
            e.printStackTrace();
        }
    }

    public static EventsController getInstance() {
        if (instance == null) {
            instance = new EventsController();
        }
        return instance;
    }

    @SuppressLint("SimpleDateFormat")
    public void initializeEvents() throws ParseException {
        addEvent(new Events(
                "EV001",
                "Markplus Conference 2018",
                "The biggest marketing event in Asia! The 12th Annual MarkPlus Conference 2018 will be held in Jakarta on 7 December 2018 at Grand Ballroom, The Ritz Carlton Jakarta!",
                "The Ritz-Carlton Jakarta",
                new SimpleDateFormat("dd/MM/yyyy").parse("7/12/2018"),
                new SimpleDateFormat("dd/MM/yyyy").parse("7/12/2018"),
                9,
                -6.228540,
                106.827174)
        );

        addEvent(new Events(
                "EV002",
                "Charity Concert",
                "Perform by Project Pop, Elephant Kind, Lex Musica, Naomi x Roma, Rumah Belajar Matalangi Yayasan PKBM Al-Falah",
                "Integrated Faculty Club, UI",
                new SimpleDateFormat("dd/MM/yyyy").parse("22/12/2018"),
                new SimpleDateFormat("dd/MM/yyyy").parse("22/12/2018"),
                8,
                -6.351236,
                106.830689)
        );

        addEvent(new Events(
                        "EV003",
                        "Incubus Lives",
                        "Incubus Live in Jakarta",
                        "Jakarta at JIExpo Kemayoran",
                        new SimpleDateFormat("dd/MM/yyyy").parse("7/2/2018"),
                        new SimpleDateFormat("dd/MM/yyyy").parse("7/2/2018"),
                        8,
                        -6.144804,
                        106.848686
                )
        );

        addEvent(new Events(
                        "EV004",
                        "Comic Con",
                        "Indonesia Comic Con",
                        "Jakarta Convention Center",
                        new SimpleDateFormat("dd/MM/yyyy").parse("28/10/2018"),
                        new SimpleDateFormat("dd/MM/yyyy").parse("29/10/2018"),
                        9,
                        -6.214078,
                        106.807378
                )
        );

        addEvent(new Events(
                        "EV005",
                        "Innovate or Die!!",
                        "Seminar and Workshop",
                        "Mh Thamrin Kav 28-30 Jakarta, Indonesia",
                        new SimpleDateFormat("dd/MM/yyyy").parse("18/1/2018"),
                        new SimpleDateFormat("dd/MM/yyyy").parse("18/1/2018"),
                        7,
                        -6.192896,
                        106.822252
                )
        );
    }

    public ArrayList<Events> getListEvents() {
        return listEvents;
    }

    public void addEvent(Events event) {
        listEvents.add(event);
    }

    public boolean isEventRegistered(String eventID) {
        boolean flag = false;

        for (Events event: listEvents) {
            if (event.getEventID().equals(eventID)) {
                flag = true;
                break;
            }
        }

        return flag;
    }

    public Events getOneEvent(String eventID) {
        int idxFound = -1;

        for (int i = 0; i < this.listEvents.size(); i++) {
            if (listEvents.get(i).getEventID().equals(eventID)) {
                idxFound = i;
                break;
            }
        }

        if (idxFound == -1) {
            return null;
        }else {
            return this.listEvents.get(idxFound);
        }
    }

    public ArrayList<Events> getTop3Events(){
        ArrayList<Events> listEventsDescRating = (ArrayList<Events>) this.listEvents.clone();

        for (int i = 0; i < listEventsDescRating.size(); i++){
            for (int j = 0; j < listEventsDescRating.size() - i - 1; j++){
                if(listEventsDescRating.get(j).getRating() < listEventsDescRating.get(j+1).getRating()){
                    Events tempEvent = listEventsDescRating.get(j+1);
                    listEventsDescRating.set(j+1, listEventsDescRating.get(j));
                    listEventsDescRating.set(j, tempEvent);
                }
            }
        }

        ArrayList<Events> listTop3Events = new ArrayList<Events>();

        for (int i = 0; i < 3; i++){
            listTop3Events.add(listEventsDescRating.get(i));
        }

        return listTop3Events;
    }

}
