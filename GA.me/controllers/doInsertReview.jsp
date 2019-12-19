<%@ include file = "connect.jsp" %>
<%
	//Get parameter from gameDetail.jsp
	String id = request.getParameter("gameId");
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
		//Post Review Success
		String query = " INSERT INTO gamedetail(UserId, GameId, Review) VALUES('"+session.getAttribute("UserId")+"','"+id+"','"+review+"')";
		st.executeUpdate(query);

		//Redirect to selected game detail
		response.sendRedirect(request.getContextPath()+"/views/gameDetail.jsp?id="+id);
	}else{
		//Post Review Failed, passing error message
		response.sendRedirect(request.getContextPath()+"/views/gameDetail.jsp?id="+id+"&errReview="+errReview);
	}
%>