package DataModel;

/**
 * Created by USER on 3/3/2018.
 */

public class Users {
    private String userID;
    private String fullname;
    private String username;
    private String password;
    private String gender;
    private String phoneNumber;
    private String address;

    public Users(String userID, String fullname, String username, String password, String gender, String phoneNumber, String address) {
        this.userID = userID;
        this.fullname = fullname;
        this.username = username;
        this.password = password;
        this.gender = gender;
        this.phoneNumber = phoneNumber;
        this.address = address;
    }

    public String getUserID() {
        return userID;
    }

    public String getFullname() {
        return fullname;
    }

    public String getUsername() {
        return username;
    }

    public String getPassword() {
        return password;
    }

    public String getGender() {
        return gender;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public String getAddress() {
        return address;
    }
}
