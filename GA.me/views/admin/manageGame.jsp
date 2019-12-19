<%
	//Only admin can access
	if(!session.getAttribute("UserRole").equals("admin")){
		response.sendRedirect(request.getContextPath()+"/views/template/badUrl.jsp");
	}
%>

<%@ include file = "../../controllers/connect.jsp" %>

<!--Pagination-->
<%
	//Get search key parameter (input by user) and search in the database
	String searchKey = "";
	String condition = "";
	if(request.getParameter("search") != null){
		searchKey = request.getParameter("search");
		condition = " WHERE GameName LIKE '%" + searchKey + "%'";
	}

	//Get total data
	String query = "SELECT COUNT(*) FROM game" + condition;
	ResultSet rs = st.executeQuery(query);
	int totalData = 0;
	if(rs.next()){
		totalData = rs.getInt(1);
	}

	//Calculate total page based on total data and how many row per page
	int gamePerPage = 6;
	int totalPage = (int)Math.ceil(totalData / (double)gamePerPage);

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
	int skipRow = (currentPage - 1)*gamePerPage;
	query = "SELECT * FROM game LEFT JOIN genre ON game.GenreID = genre.GenreID" + condition + " LIMIT " + skipRow + ", " + gamePerPage;
	rs = st.executeQuery(query);
%>

<!DOCTYPE html>
<html>
<head>
	<title>GA.me</title>
	<%@ include file = "../template/import.jsp" %>
</head>
<body>

	<!--Header Section-->
	<%@ include file = "../template/header.jsp" %>
	
	<!--Manage Game Content-->
	<div class="bg-midnight main-content">
		<div class="container py-4">
			<!--Manage Game Title-->
			<div class="row">
				<div class="col-md-10 offset-md-1">
					<h4 class="text-light font-weight-bold lead">Manage GAmes</h4>
					<p class="text-secondary">Popular game in GAme</p>
				</div>
			</div>

			<div class="row">
				<div class="col-md-1"></div>
				<div class="col-md-10 box-content">
					<div class="row">
						<!--Insert New Game Button-->
						<div class="col-md-6">
							<form action="insertGame.jsp" method="POST" class="form-inline">
								<div class="form-group">
									<input type="submit" class="btn custom-btn" value="Insert New Game">
								</div>
							</form>
						</div>

						<!--Search game by game title-->
						<div class="col-md-6">
							<form action="manageGame.jsp" method="GET" class="form-inline">
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
				</div>
			</div>

			<!--Loop Game-->
			<%
				while(rs.next())
				{
			%>
			<div class="row">
				<div class="col-md-1"></div>
				<div class="col-md-10 custom-list-item">
					<div class="row">
						<!--Game Picture-->
						<div class="col-md-3">
							<img src="../../assets/gamepictures/<%= rs.getString("GamePicture")%>" width="100%">
						</div>

						<!--Game Information-->
						<div class="col-md-5">
							<p class="text-light m-0">
								<%= rs.getString("GameName")%>									
							</p>
							<p class="text-secondary">
								<!--Validate when Genre is deleted by admin-->
								<%= rs.getString("GenreId") == null? "No Genre" : rs.getString("GenreName")%>
							</p>
						</div>

						<div class="col-md-2">
							<p class="text-light">Rp <%= rs.getString("GamePrice")%></p>
						</div>
						
						<div class="col-md-2">
							<!--Update Game Button-->
							<form action="updateGame.jsp" method="POST">
								<div class="form-group">
									<input type="hidden" name="gameId" value='<%= rs.getString("GameId") %>'>
									<input type="submit" class="btn btn-success" value="Update" style="width:100%">
								</div>
							</form>

							<!--Delete Game Button-->
							<button type="button" class="btn btn-danger deleteModal" data-toggle="modal" data-target="#deleteModal" data-game-id = "<%= rs.getString("GameId") %>" data-game-name = "<%= rs.getString("GameName") %>" style="width:100%">
								Delete
							</button>

							<!--Modal (Pop Up) for Delete-->
							<div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteModalCenterTitle" aria-hidden="true">
								<div class="modal-dialog modal-dialog-centered" role="document">
							    	<div class="modal-content">
							      		<div class="modal-header">
							        		<h5 class="modal-title" id="deleteModalLongTitle">Delete Game</h5>
							        		<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							          			<span aria-hidden="true">&times;</span>
							        		</button>
							      		</div>
									    <div class="modal-body">
									    	<!--Must assign gameName outside the while loop (in JS)-->
									    	Are you sure you want to delete <p id="gameName" class="d-inline"></p>?
									    </div>
										<div class="modal-footer">
									    	<button type="button" class="btn btn-secondary" data-dismiss="modal">No</button>
									    	<form action="../../controllers/admin/doDeleteGame.jsp" method="POST">
									    		<!--Must assign gameId value outside the while loop (in JS)-->
									    		<input type="hidden" id="gameId" name="gameId" value="">
									    		<input type="submit" class="btn btn-danger" value="Yes">
									    	</form>
									 	</div>
							    	</div>
							  	</div>
							</div>
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
							href='manageGame.jsp?page=
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
							href='manageGame.jsp?page=
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
							href='manageGame.jsp?page=
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
	<%@ include file = "../template/footer.jsp" %>

	<!-- JS for Delete Modal -->
	<script type="text/javascript">
	    $(function () {
	        $(".deleteModal").click(function () {
	            var gameId = $(this).data('game-id');
	            document.getElementById('gameId').value = gameId;

	            var gameName = $(this).data('game-name');
	            document.getElementById('gameName').innerHTML = gameName;
	        })
	    });
	</script>

</body>
</html>