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
	
	<!--Home Content-->
	<div class="bg-midnight main-content">
		<div class="container py-4">
			<!--Home Title-->
			<div class="row">
				<div class="col-md-10 offset-md-1">
					<h4 class="text-light font-weight-bold lead">Community Activity</h4>
					<p class="text-secondary">Community and official content for all games and software on GAme.</p>
				</div>
			</div>

			<!--First row content-->
			<div class="row">
				<div class="col-md-1"></div>
				<!--Caraousel (Slider)-->
				<div class="col-md-7 box-content">
					<div id="mainCarousel" class="carousel slide" data-ride="carousel" data-interval="2500">
						<div class="carousel-inner">

							<%
								//Get all gamepicture from database
								String query = " SELECT * FROM game ";
								ResultSet rs = st.executeQuery(query);
								boolean active = true; //flag for setting active on the first picture
								while(rs.next()){
							%>

					    	<div class="carousel-item <% if(active){out.println("active");} %>">
					      		<a href="../views/gameDetail.jsp?id=<%= rs.getString("GameId") %>">
					      			<img class="d-block w-100" 
					      			src="../assets/gamepictures/<%= rs.getString("GamePicture") %>"
					      			alt="<%= rs.getString("GameName")%>">
					      		</a>
					    	</div>

					    	<%
					    		active = false;
					    		}
					    	%>
					  	</div>

					  	<!--Previous button on slider-->
						<a class="carousel-control-prev" href="#mainCarousel" role="button" data-slide="prev">
							<span class="carousel-control-prev-icon" aria-hidden="true"></span>
							<span class="sr-only">Previous</span>
						</a>

						<!--Next button on slider-->
						<a class="carousel-control-next" href="#mainCarousel" role="button" data-slide="next">
							<span class="carousel-control-next-icon" aria-hidden="true"></span>
							<span class="sr-only">Next</span>
						</a>
					</div>
				</div>

				<!--Search Box-->
				<div class="col-md-3 box-content text-light">
					<!--Search Game by its name-->
					<div class="m-1">
						<form action="games.jsp" method="GET">
							<div class="form-group">
								<label>FIND GAMES</label>
								<input type="text" name="search" class="form-control custom-input" placeholder="Search for products" required>
							</div>
							<div class="form-group">
								<input type="submit" class="btn custom-btn" value="Search Game">
							</div>
						</form>
					</div>
					
					<!--Search User by its name-->
					<div class="m-1">
						<form action="community.jsp" method="GET">
							<div class="form-group">
								<label>FIND USERS</label>
								<input type="text" name="search" class="form-control custom-input" placeholder="Search for friends" required>
							</div>
							<div class="form-group">
								<input type="submit" class="btn custom-btn" value="Search User">
							</div>
						</form>
					</div>
				</div>
			</div>

			<!--Second row content-->
			<div class="row">
				<div class="col-md-1"></div>
				<div class="col-md-5 box-content">
					<a href="games.jsp" class="text-primary font-weight-bold">Instant Access to Games</a>
					<div class="row">
						<div class="col-md-8 pr-0">
							<p class="text-secondary">We have thousands of games from Action to Indie and everything in-between. Enjoy exclusive deals, automatic game updates and other great perks.</p>
						</div>
						<div class="col-md-4">
							<br>
							<img src="../assets/misc/Adventure-Time-PNG-Clipart.png" width="100%">
						</div>
					</div>
				</div>
				<div class="col-md-5 box-content">
					<a href="community.jsp" class="text-primary font-weight-bold">Join the Community</a>
					<div class="row">
						<div class="col-md-7 pr-0">
							<p class="text-secondary">Meet new people, join game groups, form clans, chat in-game and more! With over 100 million potential friends (or enemies), the fun never stops.</p>
						</div>
						<div class="col-md-5">
							<br>
							<img src="../assets/misc/Adventure-Time-PNG-HD.png" width="100%">
						</div>
					</div>

					<%
						//Display current user online count information
						int countUser = 0;
						//application.setAttribute("countUser",0);
						if(application.getAttribute("countUser") != null){
							countUser = Integer.parseInt(application.getAttribute("countUser").toString());
						}
					%>
					<p class="text-success">
						<%= countUser %> Online User
					</p>
				</div>
			</div>
		</div>
	</div>

	<!--Footer Section-->
	<%@ include file = "template/footer.jsp" %>

	<!--Start Carousel Transition-->
	<script type="text/javascript">
		$('.carousel').carousel();
	</script>

</body>
</html>