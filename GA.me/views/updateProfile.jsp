<%
	//Only logged in member can access updateProfile.jsp
	if(!session.getAttribute("UserRole").equals("member")){
		response.sendRedirect(request.getContextPath()+"/views/template/badUrl.jsp");
	}
%>

<%@ include file = "../controllers/connect.jsp" %>

<!DOCTYPE html>
<html>
<head>
	<title>GA.me</title>
	<%@ include file = "template/import.jsp" %>
</head>
<body>

	<!--Header Section-->
	<%@ include file = "template/header.jsp" %>
	
	<!--Update Profile Content-->
	<div class="bg-midnight main-content">
		<div class="container py-4">
			<!--Update Profile Title-->
			<div class="row">
				<div class="col-md-10 offset-md-1">
					<h4 class="text-light font-weight-bold lead">Update</h4>
				</div>
			</div>

			<div class="row">
				<div class="col-md-1"></div>
				<!--Update Profile Form-->

				<%
					//Get logged in user information (based on UserId session) from database
					String query = "SELECT * FROM user WHERE UserId = "+session.getAttribute("UserId");
					ResultSet rs = st.executeQuery(query);
					if(rs.next()){
				%>
				<div class="col-md-6 box-content">
					<h6 class="text-light font-weight-bold">Update</h6>
					<p class="text-secondary">Your Profile.</p>

					<form action="../controllers/doUpdateProfile.jsp" method="POST">
						<!--Name text field-->
						<div class="form-group">
							<label class="text-light">Name</label>
							<input type="text" name="txtName" class="form-control custom-input" placeholder="Name" value='<%= rs.getString("UserName") %>'>
							<span class="text-danger">
								<%
									//Display message when there is an error
									if(request.getParameter("errName")!=null){
										out.print(request.getParameter("errName"));
									}
								%>
							</span>
						</div>

						<!--Password text field-->
						<div class="form-group">
							<label class="text-light">Password</label>
							<input type="password" name="txtPassword" class="form-control custom-input" placeholder="Password" value='<%= rs.getString("UserPassword") %>'>
							<span class="text-danger">
								<%
									//Display message when there is an error
									if(request.getParameter("errPassword")!=null){
										out.print(request.getParameter("errPassword"));
									}
								%>
							</span>
						</div>

						<!--Email text field-->
						<div class="form-group">
							<label class="text-light">Email</label>
							<input type="text" name="txtEmail" class="form-control custom-input" placeholder="Email" value='<%= rs.getString("UserEmail") %>'>
							<span class="text-danger">
								<%
									//Display message when there is an error
									if(request.getParameter("errEmail")!=null){
										out.print(request.getParameter("errEmail"));
									}
								%>
							</span>
						</div>

						<!--Picture upload file button-->
						<div class="form-group">
							<label class="text-light">Picture</label><br>
							<img src='../assets/userpictures/<%= rs.getString("UserPicture") %>' width="20%">
							<input type="hidden" name="currentPicture" value='<%= rs.getString("UserPicture") %>'>
							<input type="file" name="newPicture" class="form-control custom-input">
						</div>

						<!--Update Data button-->
						<div class="form-group">
							<input type="submit" class="btn btn-success" value="Update Data">
						</div>
					</form>
				</div>
				<%
					}else{
						//When the page is accessed directly from the link
						response.sendRedirect(request.getContextPath()+"/views/template/badUrl.jsp");
					}
				%>

				<!--Content-->
				<div class="col-md-4 box-content text-light">
					<div class="m-1">
						<h6 class="text-light font-weight-bold">Why join GAme?</h6>
						<ul class="text-secondary">
							<li>Discover lots of games</li>
							<li>Join the GAme Community</li>
							<li>Find a new friends</li>
							<li>Debate with a new friends</li>
							<li>Schedule a game, tournament, or LAN party</li>
							<li>Never miss game updates, and more!</li>
						</ul>
					</div>

					<div class="m-1">
						<a href='<%= request.getContextPath() %>/views/games.jsp' class="text-primary font-weight-bold">Instant Access to Games</a>
						<p class="text-secondary">We have thousands of games from Action to Indie and everything in-between. Join us and win the game.</p>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!--Footer Section-->
	<%@ include file = "template/footer.jsp" %>

</body>
</html>