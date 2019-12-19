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
		condition = " WHERE GenreName LIKE '%" + searchKey + "%'";
	}

	//Get total data
	String query = "SELECT COUNT(*) FROM genre" + condition;
	ResultSet rs = st.executeQuery(query);
	int totalData = 0;
	if(rs.next()){
		totalData = rs.getInt(1);
	}

	//Calculate total page based on total data and how many row per page
	int genrePerPage = 6;
	int totalPage = (int)Math.ceil(totalData / (double)genrePerPage);

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
	int skipRow = (currentPage - 1)*genrePerPage;
	query = "SELECT * FROM genre" + condition + " LIMIT " + skipRow + ", " + genrePerPage;
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
	
	<!--Manage Genre Content-->
	<div class="bg-midnight main-content">
		<div class="container py-4">
			<!--Manage Genre Title-->
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
						<!--Insert New Genre Button-->
						<div class="col-md-6">
							<form action="insertGenre.jsp" method="POST" class="form-inline">
								<div class="form-group">
									<input type="submit" class="btn custom-btn" value="Insert New Genre">
								</div>
							</form>
						</div>
						<!--Search genre by its name-->
						<div class="col-md-6">
							<form action="#" method="GET" class="form-inline">
								<div class="form-group">
									<label class="text-light">Search Genres:</label>
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

			<!--Loop Genre-->
			<%
				while(rs.next())
				{
			%>
			<div class="row">
				<div class="col-md-1"></div>
				<div class="col-md-10 custom-list-item">
					<div class="row">
						<!--Genre Name-->
						<div class="col-md-10 p-4">
							<p class="text-light m-0">
								<%= rs.getString("GenreName") %>									
							</p>
						</div>

						<div class="col-md-2">
							<!--Update Genre Button-->
							<form action="updateGenre.jsp" method="POST">
								<div class="form-group">
									<input type="hidden" name="genreId" value='<%= rs.getString("GenreId") %>'>
									<input type="submit" class="btn btn-success" value="Update" style="width:100%">
								</div>
							</form>

							<!--Delete Genre Button-->
							<button type="button" class="btn btn-danger deleteModal" data-toggle="modal" data-target="#deleteModal" data-genre-id = "<%= rs.getString("GenreId") %>" data-genre-name = "<%= rs.getString("GenreName") %>" style="width:100%">
								Delete
							</button>

							<!--Modal (Pop Up) for Delete-->
							<div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteModalCenterTitle" aria-hidden="true">
								<div class="modal-dialog modal-dialog-centered" role="document">
							    	<div class="modal-content">
							      		<div class="modal-header">
							        		<h5 class="modal-title" id="deleteModalLongTitle">Delete Genre</h5>
							        		<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							          			<span aria-hidden="true">&times;</span>
							        		</button>
							      		</div>
									    <div class="modal-body">
									    	<!--Must assign genreName outside the while loop (in JS)-->
									    	Are you sure you want to delete <p id="genreName" class="d-inline"></p>?
									    </div>
										<div class="modal-footer">
									    	<button type="button" class="btn btn-secondary" data-dismiss="modal">No</button>
									    	<form action="../../controllers/admin/doDeleteGenre.jsp" method="POST">
									    		<!--Must assign genreId value outside the while loop (in JS)-->
									    		<input type="hidden" id="genreId" name="genreId" value="">
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
							href='manageGenre.jsp?page=
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
							href='manageGenre.jsp?page=
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
							href='manageGenre.jsp?page=
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
	            var genreId = $(this).data('genre-id');
	            document.getElementById('genreId').value = genreId;

	            var genreName = $(this).data('genre-name');
	            document.getElementById('genreName').innerHTML = genreName;
	        })
	    });
	</script>

</body>
</html>