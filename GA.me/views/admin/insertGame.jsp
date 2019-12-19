<%
	//Only admin can access
	if(!session.getAttribute("UserRole").equals("admin")){
		response.sendRedirect(request.getContextPath()+"/views/template/badUrl.jsp");
	}
%>

<%@ include file = "../../controllers/connect.jsp" %>

<!DOCTYPE html>
<html>
<head>
	<title>GA.me</title>
	<%@ include file = "../template/import.jsp" %>
</head>
<body>

	<!--Header Section-->
	<%@ include file = "../template/header.jsp" %>
	
	<!--Insert Game Content-->
	<div class="bg-midnight main-content">
		<div class="container py-4">
			<!--Insert Game Title-->
			<div class="row">
				<div class="col-md-10 offset-md-1">
					<h4 class="text-light font-weight-bold lead">Insert</h4>
				</div>
			</div>

			<div class="row">
				<div class="col-md-1"></div>
				<!--Insert Game Form-->
				<div class="col-md-6 box-content">
					<h6 class="text-light font-weight-bold">Create</h6>
					<p class="text-secondary">A new GAme.</p>

					<form action="../../controllers/admin/doInsertGame.jsp" method="POST">
						<!--Name text field-->
						<div class="form-group">
							<label class="text-light">Name</label>
							<input type="text" name="txtName" class="form-control custom-input" placeholder="Name">
							<span class="text-danger">
								<%
									//Display message when there is an error
									if(request.getParameter("errName")!=null){
										out.print(request.getParameter("errName"));
									}
								%>
							</span>
						</div>

						<!--Price text field-->
						<div class="form-group">
							<label class="text-light">Price</label>
							<input type="text" name="txtPrice" class="form-control custom-input" placeholder="Price">
							<span class="text-danger">
								<%
									//Display message when there is an error
									if(request.getParameter("errPrice")!=null){
										out.print(request.getParameter("errPrice"));
									}
								%>
							</span>
						</div>

						<!--Developer dropdown list-->
						<div class="form-group">
							<label class="text-light">Developer</label>
							<select class="form-control custom-input" name="selDeveloper">
								<%
									//Get all developer from database
									String query = "SELECT * FROM developer";
									ResultSet rs = st.executeQuery(query);
									while(rs.next()){
								%>
									<option value='<%= rs.getString("DeveloperId") %>'>
										<%= rs.getString("DeveloperName") %>
									</option>
								<%
									}
								%>
							</select>
							<span class="text-danger">
								<%
									//Display message when there is an error
									if(request.getParameter("errDev")!=null){
										out.print(request.getParameter("errDev"));
									}
								%>
							</span>
						</div>

						<!--Picture upload file button-->
						<div class="form-group">
							<label class="text-light">Picture</label>
							<input type="file" name="picture" class="form-control custom-input">
							<span class="text-danger">
								<%
									//Display message when there is an error
									if(request.getParameter("errPicture")!=null){
										out.print(request.getParameter("errPicture"));
									}
								%>
							</span>
						</div>

						<!--Genre dropdown list-->
						<div class="form-group">
							<label class="text-light">Genre</label>
							<select class="form-control custom-input" name="selGenre">
								<%
									//Get all genre from database
									query = "SELECT * FROM genre";
									rs = st.executeQuery(query);
									while(rs.next()){
								%>
									<option value='<%= rs.getString("GenreId") %>'>
										<%= rs.getString("GenreName") %>
									</option>
								<%
									}
								%>
							</select>
							<span class="text-danger">
								<%
									//Display message when there is an error
									if(request.getParameter("errGenre")!=null){
										out.print(request.getParameter("errGenre"));
									}
								%>
							</span>
						</div>

						<!--Description textarea-->
						<div class="form-group">
							<label class="text-light">Description</label>
							<textarea class="form-control custom-input" name="txtDesc" rows="3" placeholder="Description"></textarea>
							<span class="text-danger">
								<%
									//Display message when there is an error
									if(request.getParameter("errDesc")!=null){
										out.print(request.getParameter("errDesc"));
									}
								%>
							</span>
						</div>

						<!--Insert Game button-->
						<div class="form-group">
							<input type="submit" class="btn btn-primary" value="Insert Game">
						</div>
					</form>
				</div>

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
	<%@ include file = "../template/footer.jsp" %>

</body>
</html>