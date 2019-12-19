<%@ include file = "connect.jsp" %>
<%
	//Get parameter from gameDetail.jsp
	String gameDetailId = request.getParameter("gameDetailId");
	String gameId = request.getParameter("gameId");
	String review = request.getParameter("txtReview").trim();

	//Initialize error message
	String errReview = "";

	//Validation for review
	if(review.equals("")){
		errReview = "Review must be filled";
	}else if(review.length() <= 10){
		errReview = "Review length must more than 10 characters";
	}

	if(errReview.equals("")){
		//Update Review Success
		String query = " UPDATE gamedetail SET Review = '"+review+"' WHERE GameDetailId = "+gameDetailId;
		st.executeUpdate(query);

		//Redirect to selected game detail page
		response.sendRedirect(request.getContextPath()+"/views/gameDetail.jsp?id="+gameId);
	}else{
		//Update Review Failed, passing error message
		session.setAttribute("gameDetailId", gameDetailId); //so that gameDetailId doesn't appear in url
		response.sendRedirect(request.getContextPath()+"/views/updateReview.jsp?errReview="+errReview);
	}
%>