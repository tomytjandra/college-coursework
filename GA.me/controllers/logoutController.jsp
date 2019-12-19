<%
	//Destroy all session
	session.invalidate();

	//Redirect to login page	
	response.sendRedirect(request.getContextPath()+"/views/login.jsp");

	//Decrease Online User Counter by 1
	try{
		int countUser = Integer.parseInt(application.getAttribute("countUser").toString());
		countUser--;
		application.setAttribute("countUser", countUser);
	}catch(Exception ex){
	}
%>