<%@ include file = "../controllers/connect.jsp" %>

<!--Pagination-->
<%
	//Get search key parameter (input by user) and search in the database
	String searchKey = "";
	String condition = "";
	if(request.getParameter("search") != null){
		searchKey = request.getParameter("search");
		condition = " WHERE UserName LIKE '%" + searchKey + "%'";
	}

	//Get total data
	String query = "SELECT COUNT(*) FROM user" + condition;
	ResultSet rs = st.executeQuery(query);
	int totalData = 0;
	if(rs.next()){
		totalData = rs.getInt(1);
	}

	//Calculate total page based on total data and how many row per page
	int userPerPage = 5;
	int totalPage = (int)Math.ceil(totalData / (double)userPerPage);

	//Get current page
	int currentPage = 1;
	if(request.getParameter("page") != null){
		try{
			currentPage = Integer.parseInt(request.getParameter("page"));
		}catch(Exception ex){
			currentPage = 1;
		}
	}

	//Select row based on search key and current page
	int skipRow = (currentPage - 1)*userPerPage;
	query = "SELECT * FROM user" + condition + " LIMIT " + skipRow + ", " + userPerPage;
	rs = st.executeQuery(query);
%>

<!DOCTYPE html>
<html>
<head>
	<title>GA.me</title>
	<%@ include file = "template/import.jsp" %>
</head>
<body>

	<!--Header Section-->
	<%@ include file = "template/header.jsp" %>
	
	<!--Community Content-->
	<div class="bg-midnight main-content">
		<div class="container py-4">
			<!--Community Title-->
			<div class="row">
				<div class="col-md-10 offset-md-1">
					<h4 class="text-light font-weight-bold lead">Users</h4>
				</div>
			</div>

			<div class="row">
				<div class="col-md-1"></div>
				<!--Search user by user name-->
				<div class="col-md-10 box-content">
					<form action="community.jsp" method="GET" class="form-inline">
						<div class="form-group">
							<label class="text-light">Search users:</label>
							<input type="text" name="search" class="form-control custom-input my-0 mx-2">
						</div>
						<div class="form-group">
							<input type="submit" class="btn custom-btn" value="Search">
						</div>
					</form>
				</div>
			</div>

			<!--Loop User-->
			<%
				while(rs.next())
				{
			%>
			<div class="row">
				<div class="col-md-1"></div>
				<div class="col-md-10 custom-list-item">
					<div class="row">
						<!--User Picture, use default.png if not set-->
						<div class="col-md-2" style="text-align: center;">
							<img src="../assets/userpictures/
							<%= rs.getString("UserPicture")==null? "default.png" : rs.getString("UserPicture")%>" width="125px" height="125px">
						</div>

						<!--User Information-->
						<div class="col-md-7">
							<p class="text-light m-0"><%= rs.getString("UserName")%></p>
							<p class="text-secondary"><%= rs.getString("UserEmail")%></p>
						</div>
						<div class="col-md-3">
							<p class="text-light"><%= rs.getString("UserRole")%></p>
						</div>
					</div>
				</div>
			</div>
			<%
				}
			%>

			<!--Pagination-->
			<div class="row">
				<div class="col-md-12">
					<ul class="pagination justify-content-center">
						
						<!--Prev button, disabled when currentPage == 1-->
						<li class="page-item
							<% if(currentPage==1){out.println("disabled");} %> ">
							<a class="page-link" 
							href='community.jsp?page=
							<%= currentPage-1 %>
							<%= condition.equals("")? "" : "&search=" + request.getParameter("search")%>'>
								Prev
							</a>
						</li>
						
						<!--Loop pagination button, from 1 until totalPage-->
						<%
							for(int i=1; i<=totalPage; i++)
							{
						%>
						<li class="page-item 
							<% if(i==currentPage){out.println("active");} %> ">
							<a class="page-link" 
							href='community.jsp?page=
							<%= i %>
							<%= condition.equals("")? "" : "&search=" + request.getParameter("search")%>'>
								<%= i %>
							</a>
						</li>
						<%
							}
						%>

						<!--Next button, disabled when currentPage == totalPage-->
						<li class="page-item
							<% if(currentPage==totalPage){out.println("disabled");} %> ">
							<a class="page-link" 
							href='community.jsp?page=
							<%= currentPage+1 %>
							<%= condition.equals("")? "" : "&search=" + request.getParameter("search")%>'>
								Next
							</a>
						</li>

					</ul>
				</div>
			</div>
		</div>
	</div>

	<!--Footer Section-->
	<%@ include file = "template/footer.jsp" %>

</body>
</html>