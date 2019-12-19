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
	
	<!--Update Game Content-->
	<div class="bg-midnight main-content">
		<div class="container py-4">
			<!--Update Game Title-->
			<div class="row">
				<div class="col-md-10 offset-md-1">
					<h4 class="text-light font-weight-bold lead">Update</h4>
				</div>
			</div>

			<div class="row">
				<div class="col-md-1"></div>
				<!--Update Game Form-->

				<%
					//gameId from manageGame.jsp
					String gameId = request.getParameter("gameId");

					//gameId from doUpdateGame.jsp
					if(session.getAttribute("gameId") != null){
						gameId = session.getAttribute("gameId").toString();
						session.removeAttribute("gameId");
					}

					String query = "SELECT * FROM game WHERE GameId = "+gameId;
					ResultSet rs = st.executeQuery(query);
					if(rs.next()){
				%>
				<div class="col-md-6 box-content">
					<h6 class="text-light font-weight-bold">Update</h6>
					<p class="text-secondary">Your GAme.</p>

					<form action="../../controllers/admin/doUpdateGame.jsp" method="POST">
						<!--Name text field-->
						<div class="form-group">
							<label class="text-light">Name</label>
							<input type="text" name="txtName" class="form-control custom-input" placeholder="Name" value="<%= rs.getString("GameName") %>">
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
							<input type="text" name="txtPrice" class="form-control custom-input" placeholder="Price" value="<%= rs.getInt("GamePrice") %>">
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
									//Create new Statement and ResultSet, so that the outer st and rs is not overwritten
									String queryDev = "SELECT * FROM developer";
									Statement stDev = connect.createStatement();
									ResultSet rsDev = stDev.executeQuery(queryDev);
									while(rsDev.next()){
								%>
									<!--Select developer based on database-->
									<option value='<%= rsDev.getString("DeveloperId") %>'
									<%= rsDev.getString("DeveloperId").equals(rs.getString("DeveloperId"))? "selected" : "" %>
									>
										<%= rsDev.getString("DeveloperName") %>
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
							<label class="text-light">Picture</label><br>
							<img src='../../assets/gamepictures/<%= rs.getString("GamePicture") %>' width="50%">
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
									//Create new Statement and ResultSet, so that the outer st and rs is not overwritten
									String queryGen = "SELECT * FROM genre";
									Statement stGen = connect.createStatement();
									ResultSet rsGen = stGen.executeQuery(queryGen);
									while(rsGen.next()){
								%>
									<!--Select genre based on database-->
									<option value='<%= rsGen.getString("GenreId") %>'
									<%= rsGen.getString("GenreId").equals(rs.getString("GenreId"))? "selected" : "" %>
									>
										<%= rsGen.getString("GenreName") %>
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
							<textarea class="form-control custom-input" name="txtDesc" rows="3" placeholder="Description"><%= rs.getString("GameDescription") %></textarea>
							<span class="text-danger">
								<%
									//Display message when there is an error
									if(request.getParameter("errDesc")!=null){
										out.print(request.getParameter("errDesc"));
									}
								%>
							</span>
						</div>

						<!--Update Game button-->
						<div class="form-group">
							<input type="hidden" name="gameId" value="<%= gameId %>">
							<input type="submit" class="btn btn-success" value="Update Game">
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
	<%@ include file = "../template/footer.jsp" %>

</body>
</html>