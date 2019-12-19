<%@ include file = "../connect.jsp" %>
<%
	//Get parameter from manageDeveloper.jsp
	String developerId = request.getParameter("developerId");

	//Delete developer based on developerId
	String query = "DELETE FROM developer WHERE DeveloperId = "+developerId;
	st.executeUpdate(query);

	//Redirect to manageDeveloper.jsp
	response.sendRedirect(request.getContextPath()+"/views/admin/manageDeveloper.jsp");
%>