<%@ include file = "connect.jsp" %>

<%
	//Get parameter from login.jsp
	String email = request.getParameter("txtEmail").trim().toLowerCase(); //email is case insensitive
	String password = request.getParameter("txtPassword").trim();
	String remember = request.getParameter("cbRemember");

	//Initialize variable for session values
	String id = "";
	String name = "";
	String role = "";

	//Initialize error message
	String errMsg = "";

	//Login validation
	if(email.equals("") || password.equals("")){
		//Both field must be filled
		errMsg = "Username and password must be filled";
	}else{
		//Both field must match with the data in the database
		String query = " SELECT * FROM user WHERE UserEmail = '"+email+"' AND UserPassword = '"+password+"' ";
		ResultSet rs = st.executeQuery(query);

		if(!rs.next()){
			errMsg = "Wrong combination of Email and Password";
		}else{
			id = rs.getString("UserId");
			name = rs.getString("UserName");
			role = rs.getString("UserRole");
		}
	}

	if(errMsg.equals("")){
		//Login Success

		//Save Cookies if "Remember Me" is checked
		if(remember != null){
			Cookie cookieEmail = new Cookie("UserEmail", email);
			cookieEmail.setMaxAge(3600); //for 1 hour
			cookieEmail.setPath("/");
			response.addCookie(cookieEmail);

			Cookie cookiePassword = new Cookie("UserPassword", password);
			cookiePassword.setMaxAge(3600); //for 1 hour
			cookiePassword.setPath("/");
			response.addCookie(cookiePassword);
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
		//Login Failed, passing error message
		response.sendRedirect(request.getContextPath()+"/views/login.jsp?errMsg="+errMsg);
	}

%>