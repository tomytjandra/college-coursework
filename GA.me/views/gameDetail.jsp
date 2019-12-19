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
	
	<!--Game Detail Content-->
	<div class="bg-midnight main-content">
		<div class="container py-4">

			<div class="row">
				<div class="col-md-1"></div>
				<!--Search game by game title-->
				<div class="col-md-10 box-content">
					<form action="games.jsp" method="GET" class="form-inline">
						<div class="form-group">
							<label class="text-light">Search our GAmes:</label>
							<input type="text" name="search" class="form-control custom-input my-0 mx-2">
						</div>
						<div class="form-group">
							<input type="submit" class="btn custom-btn" value="Search">
						</div>
					</form>
				</div>
			</div>

			<%
				//Get all game information based on selected game (id from games.jsp)
				String id = request.getParameter("id");
				String query = "SELECT * FROM game LEFT JOIN developer ON game.DeveloperId = developer.DeveloperId WHERE GameId = " + id;
				ResultSet rs = st.executeQuery(query);
			%>
			<% 
				if(rs.next()){
			%>
			<div class="row">
				<div class="col-md-1"></div>
				<div class="col-md-10 box-content">
					<div class="row">
						<!--Game Picture-->
						<div class="col-md-7">
							<img src="../assets/gamepictures/<%= rs.getString("GamePicture")%>" width="100%">
						</div>

						<!--Game Information-->
						<div class="col-md-5 text-light">
							<h5><%= rs.getString("GameName") %></h5>
							<p><%= rs.getString("GameDescription") %></p>
							<!--Validate when Developer is deleted by admin-->
							<p>Developer: <%= rs.getString("DeveloperId") == null? "No Developer" : rs.getString("DeveloperName")%></p>
							<p>Price: <%= rs.getString("GamePrice") %></p>
						</div>
					</div>
				</div>
			</div>
			<%
				}else{
					//When the page is accessed directly from the link, and id is not available
					response.sendRedirect(request.getContextPath()+"/views/template/badUrl.jsp");
				}
			%>


			<%
				//Only logged in user can post a game review
				if(session.getAttribute("UserRole") != null){
					String gameName = rs.getString("GameName"); //from resultset above
					query = "SELECT * FROM user WHERE UserId = "+session.getAttribute("UserId");
					rs = st.executeQuery(query);
					rs.next();
			%>

				<div class="row">
					<div class="col-md-1"></div>
					<div class="col-md-10 box-review">
						<p class="text-primary font-weight-bold d-inline">Write review for <%=gameName%></p>
						<p class="text-secondary">Please describe what you liked or disliked about this game and whether you recommend it to others. Please remember to be polite and follow the Rules and Guidelines.</p>
						<div class="row">
							<div class="col-md-1">
								<img src='../assets/userpictures/<%= rs.getString("UserPicture") %>' width="100%">
							</div>	
							<div class="col-md-11">
								<!--Post Review Form-->
								<form action="../controllers/doInsertReview.jsp" method="POST">
									<!--Review textarea-->
									<div class="form-group">
										<textarea class="form-control custom-input" name="txtReview" rows="5"></textarea>
									</div>
									
									<!--Error Message and Post Review Button-->
									<div class="form-group text-right">
										<span class="text-danger" style="margin-right: 20px;">
										<%
											//Display message when there is an error
											if(request.getParameter("errReview")!=null){
												out.print(request.getParameter("errReview"));
											}
										%>
										</span>
										<input type="hidden" name="gameId" value="<%= id %>">
										<input type="submit" class="btn btn-primary" value="Post Review">
									</div>
								</form>
							</div>	
						</div>
					</div>
				</div>	

			<%
				}
			%>

			<!--Display review on selected games, sorted from latest to oldest review-->
			<div class="row">
				<div class="col-md-1"></div>
				<div class="col-md-10">
					<h4 class="text-secondary font-weight-bold lead">Reviews</h4>
				</div>
			</div>

			<%
				int countReview = 0;
				query = "SELECT * FROM game JOIN gamedetail ON game.GameId = gamedetail.GameId JOIN user ON user.UserId = gamedetail.UserId WHERE game.GameId = " + id + " ORDER BY PostedDate DESC";
				rs = st.executeQuery(query);

				//Loop Review
				while(rs.next())
				{
					countReview++;
			%>
			<div class="row">
				<div class="col-md-1"></div>
				<div class="col-md-10 box-content">
					<div class="row">
						<!--User picture-->
						<div class="col-md-1">
							<img src="../assets/userpictures/<%= rs.getString("UserPicture")%>" width="100%">
						</div>

						<!--Review detail-->
						<div class="col-md-9 text-light">
							<p class="text-primary font-weight-bold d-inline">
								<%= rs.getString("UserName") %>
							</p>
							<p>Posted: <%= rs.getDate("PostedDate") %></p>
							<p><%= rs.getString("Review") %></p>
						</div>

						<!--Display "Update Review" button if the review is written by the logged in user-->
						<%
							if(session.getAttribute("UserId") != null){
								String userId = session.getAttribute("UserId").toString();
								if(userId.equals(rs.getString("UserId")))
								{
						%>

							<div class="col-md-2">
								<form action="updateReview.jsp" method="POST">
									<div class="form-group">
										<input type="hidden" name="gameDetailId" value='<%= rs.getString("GameDetailId") %>'>
										<input type="submit" class="btn custom-btn" value="Update Review">
									</div>
								</form>
							</div>

						<%
								}
							}
						%>
					</div>
				</div>
			</div>
			<%
				}
			%>

			<!--Display "No Review" if the review count is 0-->
			<%
				if(countReview == 0)
				{
			%>
			<div class="row">
				<div class="col-md-1"></div>
				<div class="col-md-10 box-content text-light">
					<p>This game has no review yet.</p>
				</div>
			</div>	
			<%
				}
			%>
		</div>
	</div>

	<!--Footer Section-->
	<%@ include file = "template/footer.jsp" %>

</body>
</html>