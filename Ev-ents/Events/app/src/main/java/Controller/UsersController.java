package Controller;

import java.util.ArrayList;

import DataModel.Users;

/**
 * Created by USER on 3/10/2018.
 */

public class UsersController {
    private ArrayList<Users> listUsers;
    private static UsersController instance;
    private String currentUserID;

    public UsersController() {
        listUsers = new ArrayList<Users>();
    }

    public static UsersController getInstance() {
        if (instance == null) {
            instance = new UsersController();
        }
        return instance;
    }

    public ArrayList<Users> getListUsers() {
        return listUsers;
    }

    public void addUser(Users user) {
        listUsers.add(user);
    }

    public String getCurrentUserID() {
        return currentUserID;
    }

    public void setCurrentUserID(String currentUserID) {
        this.currentUserID = currentUserID;
    }

    public boolean isUsernameRegistered(String username) {
        boolean flag = false;

        for (Users user: listUsers) {
            if (user.getUsername().toLowerCase().equals(username.toLowerCase())) {
                flag = true;
                break;
            }
        }

        return flag;
    }

    public String searchUserID(String username, String password) {
        String userID = "";

        for (Users user: listUsers) {
            if (user.getUsername().equals(username)) {
                if (user.getPassword().equals(password)) {
                    userID = user.getUserID();
                }
                break;
            }
        }

        return userID;
    }

}
