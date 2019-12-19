<%@ include file = "connect.jsp" %>

<%!
	//Validation for email format
	public Boolean checkEmailFormat(String email){
		int countAt = 0, countDot = 0;

		for(int i=0; i<email.length(); i++){
			char c = email.charAt(i);

			//Counting '@' and '.' symbol
			if(c == '@'){
				countAt++;
			}else if(c == '.'){
				countDot++;
			}

			//'@' and '.' must not be side by side
			if(i < email.length()-1){
				if(email.charAt(i) == '@' && email.charAt(i+1) == '.'){
					return false;
				}
			}
		}

		//Contain '@' and '. symbol
		//Contain only one '@' symbol
		if(countAt == 1 && countDot > 0){
			return true;
		}else{
			return false;
		}
	}

	//Validation for name (must be alphabet)
	public Boolean isAlphabetLetters(String name){
		for(int i=0; i<name.length(); i++){
			char c = name.charAt(i);

			if(!Character.isLetter(c)){
				return false;
			}
		}
		return true;
	}

	//Validation for password format
	public Boolean checkPasswordFormat(String password){
		int countSymbol = 0, countLetter = 0, countNumber = 0;

		for(int i=0; i<password.length(); i++){
			char c = password.charAt(i);

			if(!Character.isLetter(c) && !Character.isDigit(c) && !Character.isSpace(c)){
				countSymbol++;
			}else if(Character.isLetter(c)){
				countLetter++;
			}else if(Character.isDigit(c)){
				countNumber++;
			}
		}

		if(countSymbol==0 || countLetter==0 || countNumber==0){
			return false;
		}else{
			return true;
		}
	}
%>

<%
	//Get parameter from updateProfile.jsp
	String name = request.getParameter("txtName").trim();
	String email = request.getParameter("txtEmail").trim().toLowerCase(); //email is case insensitive
	String password = request.getParameter("txtPassword").trim();
	String currentPicture = request.getParameter("currentPicture");
	String newPicture = request.getParameter("newPicture");

	//Initialize error message
	String errName = "";
	String errEmail = "";
	String errPassword = "";

	//Validation for name
	if(name.equals("")){
		errName = "Name must be filled";
	}else if(name.length() < 5 || name.length() > 20){
		errName = "Name length must be between 5 and 20 characters";
	}else if(!isAlphabetLetters(name)){
		errName = "Name must be alphabet letters only";
	}

	//Validation for email
	if(email.equals("")){
		errEmail = "Email must be filled";
	}else if(email.length() <= 4){
		errEmail = "Email length must be more than 4 characters";
	}else if(!checkEmailFormat(email)){
		errEmail = "Wrong email format";
	}else if(!email.equals(session.getAttribute("UserEmail"))){
		//Check email must not be registered
		String query = " SELECT * FROM user WHERE UserEmail = '"+email+"' ";
		ResultSet rs = st.executeQuery(query);

		if(rs.next()){
			errEmail = "Email is already registered";
		}
	}

	//Validation for password
	if(password.equals("")){
		errPassword = "Password must be filled";
	}else if(password.length() <= 8){
		errPassword = "Password length must be more than 8 characters";
	}else if(!checkPasswordFormat(password)){
		errPassword = "Password must contain symbol, letter, and number";
	}

	//If user not upload a new picture, then use current picture
	if(newPicture.equals("")){
		newPicture = currentPicture;
	}

	if(errName.equals("") && errEmail.equals("") && errPassword.equals("")){
		//Update Success
		String query = " UPDATE user SET Username = '"+name+"', UserEmail = '"+email+"', UserPassword = '"+password+"', UserPicture = '"+newPicture+"' WHERE UserId = "+session.getAttribute("UserId");
		st.executeUpdate(query);

		//Redirect to home
		response.sendRedirect(request.getContextPath()+"/views/home.jsp");
	}else{
		//Update Failed, passing error message
		response.sendRedirect(request.getContextPath()+"/views/updateProfile.jsp?errEmail="+errEmail+"&errPassword="+errPassword+"&errName="+errName);
	}
	
%>