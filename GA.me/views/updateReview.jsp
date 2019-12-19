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
	
	<!--Update Review Content-->
	<div class="bg-midnight main-content">
		<div class="container py-4">
			<!--Update Review Title-->
			<div class="row">
				<div class="col-md-10 offset-md-1">
					<h4 class="text-light font-weight-bold lead">Update</h4>
				</div>
			</div>

			<div class="row">
				<div class="col-md-1"></div>
				<!--Update Review Form-->

				<%
					//gameDetailId from gameDetail.jsp
					String gameDetailId = request.getParameter("gameDetailId"); 

					//gameDetailId from doUpdateReview.jsp
					if(session.getAttribute("gameDetailId") != null){
						gameDetailId = session.getAttribute("gameDetailId").toString(); 
						session.removeAttribute("gameDetailId");
					}

					String query = "SELECT * FROM gamedetail JOIN game ON gamedetail.GameId = game.GameId JOIN user ON gamedetail.UserId = user.UserId WHERE GameDetailId = "+gameDetailId;
					ResultSet rs = st.executeQuery(query);
					if(rs.next())
					{
				%>
				<div class="col-md-6 box-content">
					<p class="text-primary font-weight-bold d-inline">Update a review for <%= rs.getString("GameName") %></p>
					<p class="text-secondary">Please describe what you liked or disliked about this game and whether you recommend it to others. Please remember to be polite and follow the Rules and Guidelines.</p>
					<div class="row">
						<div class="col-md-2">
							<img src='../assets/userpictures/<%= rs.getString("UserPicture") %>' width="100%">
						</div>	
						<div class="col-md-10">
							<form action="../controllers/doUpdateReview.jsp" method="POST">
								<!--Review text area-->
								<div class="form-group">
									<textarea class="form-control custom-input" name="txtReview" rows="5"><%= rs.getString("Review") %></textarea>
								</div>

								<!--Error Message and Edit Review Button-->
								<div class="form-group text-right">
									<span class="text-danger" style="margin-right: 20px;">
									<%
										//Display message when there is an error
										if(request.getParameter("errReview")!=null){
											out.print(request.getParameter("errReview"));
										}
									%>
									</span>
									<input type="hidden" name="gameDetailId" value='<%= gameDetailId %>'>
									<input type="hidden" name="gameId" value='<%= rs.getString("GameId") %>'>
									<input type="submit" class="btn btn-success" value="Edit Review">
								</div>
							</form>
						</div>	
					</div>
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
						<a href="games.jsp" class="text-primary font-weight-bold">Instant Access to Games</a>
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