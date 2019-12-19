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
	//Get parameter from register.jsp
	String email = request.getParameter("txtEmail").trim().toLowerCase(); //email is case insensitive
	String password = request.getParameter("txtPassword").trim();
	String name = request.getParameter("txtName").trim();

	//Initialize error message
	String errEmail = "";
	String errPassword = "";
	String errName = "";

	//Validation for email
	if(email.equals("")){
		errEmail = "Email must be filled";
	}else if(email.length() <= 4){
		errEmail = "Email length must be more than 4 characters";
	}else if(!checkEmailFormat(email)){
		errEmail = "Wrong email format";
	}else{
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

	//Validation for name
	if(name.equals("")){
		errName = "Name must be filled";
	}else if(name.length() < 5 || name.length() > 20){
		errName = "Name length must be between 5 and 20 characters";
	}else if(!isAlphabetLetters(name)){
		errName = "Name must be alphabet letters only";
	}

	if(errEmail.equals("") && errPassword.equals("") && errName.equals("")){
		//Register Success
		String role = "member";
		
		//Insert user to database
		String query = " INSERT INTO user(UserEmail, UserPassword, UserName, UserRole) VALUES('"+email+"', '"+password+"', '"+name+"', '"+role+"') ";
		st.executeUpdate(query);

		//Get the user id (for session)
		query = "SELECT MAX(UserId) FROM user";
		ResultSet rs = st.executeQuery(query);
		int id = 0;
		if(rs.next()){
			id = rs.getInt(1);
		}

		//Save Session
		session.setAttribute("UserId", id);
		session.setAttribute("UserName", name);
		session.setAttribute("UserRole", role);
		session.setAttribute("UserEmail", email);

		//Add Online User Counter by 1
		int countUser = 0;
		if(application.getAttribute("countUser") != null){
			countUser = Integer.parseInt(application.getAttribute("countUser").toString());
		}
		countUser++;
		application.setAttribute("countUser", countUser);

		//Redirect to home
		response.sendRedirect(request.getContextPath()+"/views/home.jsp");
	}else{
		//Register Failed, passing error message
		response.sendRedirect(request.getContextPath()+"/views/register.jsp?errEmail="+errEmail+"&errPassword="+errPassword+"&errName="+errName);
	}
	
%>