<%@ include file = "../connect.jsp" %>

<%!
	//Validation for price (must be numeric)
	public Boolean isNumeric(String price){
		//Better not to use looping because the price can contain "-" sign
		try{
			Integer.parseInt(price);
			return true;
		}catch(Exception e){
			return false;
		}
	}

	//Validation for picture (file extension)
	public Boolean checkFileExtension(String picture){
		int dotIdx = picture.indexOf('.');
		String ext = picture.substring(dotIdx, picture.length()).toLowerCase();

		if(ext.equals(".png") ||ext.equals(".jpg")){
			return true;
		}else{
			return false;
		}
	}
%>

<%
	//Get parameter from updateGame.jsp
	String gameId = request.getParameter("gameId");
	String name = request.getParameter("txtName");
	String price = request.getParameter("txtPrice");
	String developerId = request.getParameter("selDeveloper");
	String picture = request.getParameter("picture");
	String genreId = request.getParameter("selGenre");
	String description = request.getParameter("txtDesc");

	//Initialize error message
	String errName = "";
	String errPrice = "";
	String errPicture = "";
	String errDesc = "";
	//note: Developer and Genre are not validated because it is already guaranteed that admin can only select the existing data from database

	//Validation for name
	if(name.equals("")){
		errName = "Name must be filled";
	}else if(name.length() >= 50){
		errName = "Name length must be less than 50 characters";
	}

	//Validation for price
	if(price.equals("")){
		errPrice = "Price must be filled";
	}else if(!isNumeric(price)){
		errPrice = "Price must be numeric";
	}else if(Integer.parseInt(price) <= 0){
		errPrice = "Price must be more than 0";
	}

	//Validation for picture
	if(picture.equals("")){
		errPicture = "Picture must be selected";
	}else if(!checkFileExtension(picture)){
		errPicture = "File extension must be either .png or .jpg";
	}

	//Validation for description
	if(description.equals("")){
		errDesc = "Description must be filled";
	}else if(description.length() >= 255){
		errDesc = "Description length must be less than 255 characters";
	}

	if(errName == "" && errPrice == "" && errPicture == "" && errDesc == ""){
		//Update Game Success
		String query = " UPDATE game SET GameName = '"+name+"', GamePrice = "+price+", DeveloperId = "+developerId+", GamePicture = '"+picture+"', GenreId = "+genreId+", GameDescription = '"+description+"' WHERE GameId = "+gameId;
		st.executeUpdate(query);

		//Redirect to manageGame.jsp
		response.sendRedirect(request.getContextPath()+"/views/admin/manageGame.jsp");
	}else{
		//Update Game Failed, passing error message
		session.setAttribute("gameId", gameId); //so that gameId doesn't appear in url
		response.sendRedirect(request.getContextPath()+"/views/admin/updateGame.jsp?errName="+errName+"&errPrice="+errPrice+"&errPicture="+errPicture+"&errDesc="+errDesc);
	}
%>