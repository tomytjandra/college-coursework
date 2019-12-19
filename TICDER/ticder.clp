;GLOBAL VARIABLE
(defglobal 
    ?*countMale* = 0
    ?*countFemale* = 0
 )

;DEFTEMPLATE
(deftemplate male 
    (slot name)
    (slot age)
    (slot hobby)
    (slot interest)
    (slot height)
    (slot income)
)

(deftemplate female 
    (slot name)
    (slot age)
    (slot hobby)
    (slot interest)
    (slot height)
)

(deftemplate matchUser
    (slot name)
    (slot age)
    (slot gender)
    (slot height)
    (slot hobby)
    (slot interest)
    (slot preferredIncome)
)

(deftemplate matchMale 
    (slot name)
    (slot age)
    (slot hobby)
    (slot interest)
    (slot height)
    (slot income)
    (slot match-rate)
)

(deftemplate matchFemale 
    (slot name)
    (slot age)
    (slot hobby)
    (slot interest)
    (slot height)
    (slot match-rate)
)

;DEFFACTS
(deffacts initializeMale
    (male (name "Calvin")	(age 20)	(hobby "Game")	(interest "Female")	(height 170) (income 600))
	(male (name "Vincent")	(age 18)	(hobby "Sport")	(interest "Female")	(height 165) (income 450))
	(male (name "Bambang")	(age 33)	(hobby "Music")	(interest "Female")	(height 175) (income 200))
	(male (name "David")	(age 69)	(hobby "Sport")	(interest "Male")	(height 159) (income 1000))
	(male (name "Cristian")	(age 27)	(hobby "Game")	(interest "Female")	(height 192) (income 50))
)

(deffacts initializeFemale
    (female (name "Cindy")		(age 18)	(hobby "Music")	(interest "Male")	(height 150))
	(female (name "Jennifer")	(age 50)	(hobby "Game")	(interest "Female")	(height 190))
	(female (name "Tukiyem")	(age 99)	(hobby "Sport")	(interest "Male")	(height 167))
	(female (name "Elis")		(age 32)	(hobby "Music")	(interest "Male")	(height 170))
	(female (name "Yolanda")	(age 28)	(hobby "Game")	(interest "Male")	(height 164))
)

;DEFRULE
(defrule printMale
	(printMale)
    (male (name ?name) (age ?age) (hobby ?hobby) (interest ?interest) (height ?height) (income ?income))
    =>
    (++ ?*countMale*)
    (format t "| %-2d. | %-20s | %-5d | %-10s | %-10s | %8dcm | %11d$USD |%n" ?*countMale* ?name ?age ?hobby ?interest ?height ?income)
)

(defrule printFemale
	(printFemale)
    (female (name ?name) (age ?age) (hobby ?hobby) (interest ?interest) (height ?height))
    =>
    (++ ?*countFemale*)
    (format t "| %-2d. | %-20s | %-5d | %-10s | %-10s | %8dcm |%n" ?*countFemale* ?name ?age ?hobby ?interest ?height)
)

(defrule updateMale
    ?trig <- (updateMale ?index ?newName ?newAge ?newHobby ?newInterest ?newHeight ?newIncome)
    ?updatedFact <- (male (name ?name) (age ?age) (hobby ?hobby) (interest ?interest) (height ?height) (income ?income))
    =>
    (++ ?*countMale*)
    (
        if (eq ?index ?*countMale*) then
        	(modify ?updatedFact (name ?newName) (age ?newAge) (hobby ?newHobby) (interest ?newInterest) (height ?newHeight) (income ?newIncome))
    		(retract ?trig)
    )
)

(defrule updateFemale
    ?trig <- (updateFemale ?index ?newName ?newAge ?newHobby ?newInterest ?newHeight)
    ?updatedFact <- (female (name ?name) (age ?age) (hobby ?hobby) (interest ?interest) (height ?height))
    =>
    (++ ?*countFemale*)
    (
        if (eq ?index ?*countFemale*) then
        	(modify ?updatedFact (name ?newName) (age ?newAge) (hobby ?newHobby) (interest ?newInterest) (height ?newHeight))
        	(retract ?trig)
    )
)

(defrule deleteMale
    ?trig <- (deleteMale ?index)
    ?deletedFact <- (male (name ?name) (age ?age) (hobby ?hobby) (interest ?interest) (height ?height) (income ?income))
    =>
    (++ ?*countMale*)
    (
        if (eq ?index ?*countMale*) then
        	(retract ?deletedFact)
        	(retract ?trig)
    )
)

(defrule deleteFemale
    ?trig <- (deleteFemale ?index)
    ?deletedFact <- (female (name ?name) (age ?age) (hobby ?hobby) (interest ?interest) (height ?height))
    =>
    (++ ?*countFemale*)
    (
        if (eq ?index ?*countFemale*) then
        	(retract ?deletedFact)
        	(retract ?trig)
    )
)

;Defrule for search match menu if user interest is Male
(defrule searchMale
    (searchMale)
	(matchUser (interest "Male"))
    (male (name ?name) (age ?age) (hobby ?hobby) (interest ?interest) (height ?height) (income ?income))
    =>    
    (assert (matchMale (name ?name) (age ?age) (hobby ?hobby) (interest ?interest) (height ?height) (income ?income)))
	(assert (searchMale-byAge))
)
(defrule searchMale-byAge
    (searchMale-byAge)
	(matchUser (age ?userAge))
    ?male <- (matchMale (age ?age))
    =>
    (bind ?ageGap (abs (- ?userAge ?age)))
    (
        if(not (< ?ageGap 40)) then
        	(retract ?male)
        else
        	(assert (searchMale-byInterest))
    )  
)
(defrule searchMale-byInterest
    (searchMale-byInterest)
	(matchUser (gender ?userGender))
    ?male <- (matchMale (interest ?interest))
    =>
    (
        if(neq ?userGender ?interest) then
        	(retract ?male)
        else
        	(assert (searchMale-byHeight))
    )
)
(defrule searchMale-byHeight
    (searchMale-byHeight)
	(matchUser (height ?userHeight))
    ?male <- (matchMale (height ?height))
    =>
    (bind ?heightGap (abs (- ?userHeight ?height)))
    (
        if(not (< ?heightGap 40)) then
        	(retract ?male)
        else
        	(assert (searchMale-computeMatchRate))
    )
)
(defrule searchMale-computeMatchRate
    (searchMale-computeMatchRate)
    (matchUser (hobby ?userHobby) (age ?userAge) (height ?userHeight) (preferredIncome ?preferredIncome))
    ?male <- (matchMale (name ?name) (age ?age) (hobby ?hobby) (interest ?interest) (height ?height) (income ?income))
    =>
    ;Initial match rate value is 100
    (bind ?match-rate 100)

    ;Decrease by hobby
    (
        if (neq ?userHobby ?hobby) then
        (bind ?match-rate (- ?match-rate 20))
    )
    
    ;Decrease by age gap
    (bind ?ageGap (abs (- ?userAge ?age)))
    (bind ?match-rate (- ?match-rate ?ageGap))
    
    ;Decrease by height gap
    (bind ?heightGap (abs (- ?userHeight ?height)))
    (bind ?match-rate (- ?match-rate ?heightGap))
    
    ;Decrease by income gap
    (
        if (< ?income ?preferredIncome) then
        	(bind ?incomeGap (abs (- ?preferredIncome ?income)))
    		(bind ?match-rate (- ?match-rate ?incomeGap))
    )
    
    ;Exclude member if match rate < 0
    (
        if (< ?match-rate 0) then
        	(retract ?male)
        else
        	(modify ?male (match-rate ?match-rate))
    )
)
(defrule searchMale-retractUser
    (searchMale-retractUser)
    ?user <- (matchUser)
    =>
    (retract ?user)
    (retract-string "(searchMale)")
	(retract-string "(searchMale-byAge)")
	(retract-string "(searchMale-byInterest)")
	(retract-string "(searchMale-byHeight)")
	(retract-string "(searchMale-computeMatchRate)")
	(retract-string "(searchMale-retractUser)")
    (assert (searchMale-done))
)
(defrule searchMale-done
    (searchMale-done)
    ?male <- (matchMale)
    =>
    (retract ?male)
)

;Defrule for search match menu if user interest is Female
(defrule searchFemale
    (searchFemale)
	(matchUser (interest "Female"))
    (female (name ?name) (age ?age) (hobby ?hobby) (interest ?interest) (height ?height))
    =>    
    (assert (matchFemale (name ?name) (age ?age) (hobby ?hobby) (interest ?interest) (height ?height)))
	(assert (searchFemale-byAge))
)
(defrule searchFemale-byAge
    (searchFemale-byAge)
	(matchUser (age ?userAge))
    ?female <- (matchFemale (age ?age))
    =>
    (bind ?ageGap (abs (- ?userAge ?age)))
    (
        if(not (< ?ageGap 40)) then
        	(retract ?female)
        else
        	(assert (searchFemale-byInterest))
    )  
)
(defrule searchFemale-byInterest
    (searchFemale-byInterest)
	(matchUser (gender ?userGender))
    ?female <- (matchFemale (interest ?interest))
    =>
    (
        if(neq ?userGender ?interest) then
        	(retract ?female)
        else
        	(assert (searchFemale-byHeight))
    )
)
(defrule searchFemale-byHeight
    (searchFemale-byHeight)
	(matchUser (height ?userHeight))
    ?female <- (matchFemale (height ?height))
    =>
    (bind ?heightGap (abs (- ?userHeight ?height)))
    (
        if(not (< ?heightGap 40)) then
        	(retract ?female)
        else
        	(assert (searchFemale-computeMatchRate))
    )
)
(defrule searchFemale-computeMatchRate
    (searchFemale-computeMatchRate)
    (matchUser (hobby ?userHobby) (age ?userAge) (height ?userHeight))
    ?female <- (matchFemale (name ?name) (age ?age) (hobby ?hobby) (interest ?interest) (height ?height))
    =>
    ;Initial match rate value is 100
    (bind ?match-rate 100)
    
    ;Decrease by hobby
    (
        if (neq ?userHobby ?hobby) then
        (bind ?match-rate (- ?match-rate 20))
    )
    
    ;Decrease by age gap
    (bind ?ageGap (abs (- ?userAge ?age)))
    (bind ?match-rate (- ?match-rate ?ageGap))
    
    ;Decrease by height gap
    (bind ?heightGap (abs (- ?userHeight ?height)))
    (bind ?match-rate (- ?match-rate ?heightGap))
    
    ;Exclude member if match rate < 0
    (
        if (< ?match-rate 0) then
        	(retract ?female)
        else
        	(modify ?female (match-rate ?match-rate))
    )
)
(defrule searchFemale-retractUser
    (searchFemale-retractUser)
    ?user <- (matchUser)
    =>
    (retract ?user)
    (retract-string "(searchFemale)")
	(retract-string "(searchFemale-byAge)")
	(retract-string "(searchFemale-byInterest)")
	(retract-string "(searchFemale-byHeight)")
	(retract-string "(searchFemale-computeMatchRate)")
	(retract-string "(searchFemale-retractUser)")
    (assert (searchFemale-done))
)
(defrule searchFemale-done
    (searchFemale-done)
    ?female <- (matchFemale)
    =>
    (retract ?female)
)

;DEFFUNCTION
(deffunction clearScreen()
    (
        for (bind ?i 0) (< ?i 50) (++ ?i)
        (printout t crlf)
    )
)

(deffunction viewMale()
    (bind ?*countMale* 0)
	(printout t "List of Male Member" crlf)
	(printout t "===============================================================================================" crlf)
	(format t "| %-2s. | %-20s | %-5s | %-10s | %-10s | %-10s | %-15s |%n" "No" "Name" "Age" "Hobby" "Interest" "Height" "Income")
	(printout t "===============================================================================================" crlf)
	;Loop male facts
    (assert (printMale))
	(run)
	(retract-string "(printMale)")
	(printout t "===============================================================================================" crlf)
)
    
(deffunction viewFemale()
    (bind ?*countFemale* 0)
	(printout t "List of Female Member" crlf)
	(printout t "=============================================================================" crlf)
	(format t "| %-2s. | %-20s | %-5s | %-10s | %-10s | %-10s |%n" "No" "Name" "Age" "Hobby" "Interest" "Height")
	(printout t "=============================================================================" crlf)
	;Loop female facts
    (assert (printFemale))
	(run)
	(retract-string "(printFemale)")
	(printout t "=============================================================================" crlf)
)

(deffunction menu1()
    (bind ?chooseMenu1 -1)
	(while (neq ?chooseMenu1 0)
    	(clearScreen)
    	(printout t "List of our member to be viewed" crlf)
    	(printout t "===============================" crlf)
    	(printout t "1. Male" crlf)
    	(printout t "2. Female" crlf)
    
    	(bind ?chooseMenu1 -1)
    	(while (or (< ?chooseMenu1 0)(> ?chooseMenu1 2))
			(printout t ">> Choose [1..2 | 0 back to main menu]: ")
			(bind ?chooseMenu1 (read))

			(
	        	if(eq (numberp ?chooseMenu1) FALSE) then
	        		(bind ?chooseMenu1 -1)
	    	)
		)
    	
    	(clearScreen)
    	(
        	if(eq ?chooseMenu1 1) then
            	(viewMale)
        		(printout t "Press ENTER to continue ...")
    			(readline)
        	elif(eq ?chooseMenu1 2) then
        		(viewFemale)
        		(printout t "Press ENTER to continue ...")
    			(readline)
        )
    	(break)
    )
)

(deffunction menu2()
	(bind ?chooseMenu2 -1)
    (while (neq ?chooseMenu2 0)
        (clearScreen)
        (printout t "Types of members to be added" crlf)
        (printout t "============================" crlf)
        (printout t "1. Male" crlf)
        (printout t "2. Female" crlf)
        
    	(bind ?chooseMenu2 -1)
    	(while (or (< ?chooseMenu2 0)(> ?chooseMenu2 2))
			(printout t ">> Choose [1..2 | 0 back to main menu]: ")
			(bind ?chooseMenu2 (read))

			(
	        	if(eq (numberp ?chooseMenu2) FALSE) then
	        		(bind ?chooseMenu2 -1)
	    	)
		)
    
        ;Back to main menu if chosen menu is 0
    	(if (eq ?chooseMenu2 0) then (break))
    
    	(clearScreen)
    
        ;Input and validate name
    	(bind ?name "")
		(while (or (< (str-length ?name) 3) (> (str-length ?name) 20))
    		(printout t "Input the name [3 - 20 characters length]: ")
    		(bind ?name (readline))
    	)		

        ;Input and validate age
		(bind ?age 0)
		(while (or (< ?age 16) (> ?age 80))
    		(printout t "Input " ?name "'s age [16 - 80](years): ")
    		(bind ?age (read))
    		
    		(
        		if (eq (integerp ?age) FALSE) then
        			(bind ?age 0)
        	)
    	)

        ;Input and validate hobby
		(bind ?hobby "")
		(while (and (and (neq ?hobby "Sport") (neq ?hobby "Music")) (neq ?hobby "Game"))
    		(printout t "Input " ?name "'s hobby [ Sport | Music | Game ](CASE-SENSITIVE): ")
    		(bind ?hobby (readline))
    	)

        ;Input and validate interest
		(bind ?interest "")
		(while (and (neq ?interest "Male") (neq ?interest "Female"))
    		(printout t "Input " ?name "'s relationship preference [ Male | Female ](CASE-SENSITIVE): ")
    		(bind ?interest (readline))
    	)

        ;Input and validate height
		(bind ?height 0)
		(while (or (< ?height 100) (> ?height 240))
    		(printout t "Input " ?name "'s height [100 - 240](cm): ")
    		(bind ?height (read))
    		
    		(
        		if (eq (integerp ?height) FALSE) then
        			(bind ?height 0)
        	)
    	)
 
    	(
        	if(eq ?chooseMenu2 1) then  
            	;Input and validate income (if chosen menu is Male)  		                
        		(bind ?income -1)
        		(while (or (< ?income 0) (> ?income 10000))
            		(printout t "Input " ?name "'s income [0 - 10000]($USD): ")
            		(bind ?income (read))
            		
            		(
                		if (eq (integerp ?income) FALSE) then
                			(bind ?income -1)
                	)
            	)
        
            	;Insert male facts
        		(assert (male (name ?name) (age ?age) (hobby ?hobby) (interest ?interest) (height ?height) (income ?income)))
        		(printout t "Successfully added!" crlf)
        		(printout t "Press ENTER to continue ...")
        		(readline)
        	elif(eq ?chooseMenu2 2) then    
            	;Insert female facts
        		(assert (female (name ?name) (age ?age) (hobby ?hobby) (interest ?interest) (height ?height)))
        		(printout t "Successfully added!" crlf)
        		(printout t "Press ENTER to continue ...")
        		(readline)
        )
    	(break)
    )
)

(deffunction menu3()
	(bind ?chooseMenu3 -1)
	(while (neq ?chooseMenu3 0)
    	(clearScreen)
    	(printout t "List of our member to be updated" crlf)
    	(printout t "===============================" crlf)
    	(printout t "1. Male" crlf)
    	(printout t "2. Female" crlf)
    
    	(bind ?chooseMenu3 -1)
    	(while (or (< ?chooseMenu3 0)(> ?chooseMenu3 2))
			(printout t ">> Choose [1..2 | 0 back to main menu]: ")
			(bind ?chooseMenu3 (read))

			(
	        	if(eq (numberp ?chooseMenu3) FALSE) then
	        		(bind ?chooseMenu3 -1)
	    	)
		)
    
        ;Back to main menu if chosen menu is 0
    	(if (eq ?chooseMenu3 0) then (break))
    
    	(clearScreen)
    	
    	(bind ?idxUpdate -1)
    	(
        	if(eq ?chooseMenu3 1) then
            	(viewMale)
        		
            	;Input and validate index male member to be updated
        		(while (or (< ?idxUpdate 0) (> ?idxUpdate ?*countMale*))
            		(printout t "Which member to be updated [1.." ?*countMale* " | 0 back to main menu]: ")
            		(bind ?idxUpdate (read))
            		
            		(
                		if(eq (integerp ?idxUpdate) FALSE) then
                		(bind ?idxUpdate -1)
                	)
            	)
        
        	elif(eq ?chooseMenu3 2) then
        		(viewFemale)
        		
            	;Input and validate index female member to be updated
        		(while (or (< ?idxUpdate 0) (> ?idxUpdate ?*countFemale*))
            		(printout t "Which member to be updated [1.." ?*countFemale* " | 0 back to main menu]: ")
            		(bind ?idxUpdate (read))
            		
            		(
                		if(eq (integerp ?idxUpdate) FALSE) then
                		(bind ?idxUpdate -1)
                	)
            	)
        )
    
    	(
        	if (neq ?idxUpdate 0) then
            	;Input and validate name
        		(bind ?name "")
        		(while (or (< (str-length ?name) 3) (> (str-length ?name) 20))
            		(printout t "Input the name [3 - 20 characters length]: ")
            		(bind ?name (readline))
            	)		
        
            	;Input and validate age
        		(bind ?age 0)
        		(while (or (< ?age 16) (> ?age 80))
            		(printout t "Input " ?name "'s age [16 - 80](years): ")
            		(bind ?age (read))
            		
            		(
                		if (eq (integerp ?age) FALSE) then
                			(bind ?age 0)
                	)
            	)
        
            	;Input and validate hobby
        		(bind ?hobby "")
        		(while (and (and (neq ?hobby "Sport") (neq ?hobby "Music")) (neq ?hobby "Game"))
            		(printout t "Input " ?name "'s hobby [ Sport | Music | Game ](CASE-SENSITIVE): ")
            		(bind ?hobby (readline))
            	)
        
            	;Input and validate interest
        		(bind ?interest "")
        		(while (and (neq ?interest "Male") (neq ?interest "Female"))
            		(printout t "Input " ?name "'s relationship preference [ Male | Female ](CASE-SENSITIVE): ")
            		(bind ?interest (readline))
            	)
        
            	;Input and validate height
        		(bind ?height 0)
        		(while (or (< ?height 100) (> ?height 240))
            		(printout t "Input " ?name "'s height [100 - 240](cm): ")
            		(bind ?height (read))
            		
            		(
                		if (eq (integerp ?height) FALSE) then
                			(bind ?height 0)
                	)
            	)
        
        		(
            		if (eq ?chooseMenu3 1) then
                		;Input and validate income (if chosen menu is Male)
            			(bind ?income -1)
		        		(while (or (< ?income 0) (> ?income 10000))
		            		(printout t "Input " ?name "'s income [0 - 10000]($USD): ")
		            		(bind ?income (read))
		            		
		            		(
		                		if (eq (integerp ?income) FALSE) then
		                			(bind ?income -1)
		                	)
		            	)
		        
                		;Update male based on index
		    			(bind ?*countMale* 0)
            			(assert (updateMale ?idxUpdate ?name ?age ?hobby ?interest ?height ?income))
            			(run)    		
            
		        		(printout t "Male member with id: " ?idxUpdate " => successfully updated!" crlf)
		        		(printout t "Press ENTER to continue ...")
		        		(readline)
            		elif (eq ?chooseMenu3 2) then
                		;Update female based on index
            			(bind ?*countFemale* 0)
            			(assert (updateFemale ?idxUpdate ?name ?age ?hobby ?interest ?height))
            			(run)
            
		        		(printout t "Female member with id: " ?idxUpdate " => successfully updated!" crlf)
		        		(printout t "Press ENTER to continue ...")
		        		(readline)
            	)
        )  
    	(break)
    )
)

(deffunction menu4()
	(bind ?chooseMenu4 -1)
	(while (neq ?chooseMenu4 0)
    	(clearScreen)
    	(printout t "List of our member to be deleted" crlf)
    	(printout t "================================" crlf)
    	(printout t "1. Male" crlf)
    	(printout t "2. Female" crlf)
            
    	(bind ?chooseMenu4 -1)
    	(while (or (< ?chooseMenu4 0)(> ?chooseMenu4 2))
			(printout t ">> Choose [1..2 | 0 back to main menu]: ")
			(bind ?chooseMenu4 (read))

			(
	        	if(eq (numberp ?chooseMenu4) FALSE) then
	        		(bind ?chooseMenu4 -1)
	    	)
		)
    	
    	(clearScreen)
    	(
        	if(eq ?chooseMenu4 1) then
            	(viewMale)
        		
            	;Input and validate index male member to be deleted
        		(bind ?idxDelete -1)
        		(while (or (< ?idxDelete 0) (> ?idxDelete ?*countMale*))
            		(printout t "Which member to be deleted [1.." ?*countMale* " | 0 back to main menu]: ")
            		(bind ?idxDelete (read))
            		
            		(
                		if(eq (integerp ?idxDelete) FALSE) then
                		(bind ?idxDelete -1)
                	)
            	)
      
            	;Delete male member based on index
        		(
            		if (neq ?idxDelete 0) then
		        		(bind ?*countMale* 0)
            			(assert (deleteMale ?idxDelete))
						(run)
            
		        		(printout t "Male member with id: " ?idxDelete " => successfully deleted!" crlf)
		        		(printout t "Press ENTER to continue ...")
		        		(readline)
            	)
        
        	elif(eq ?chooseMenu4 2) then
        		(viewFemale)
        		
            	;Input and validate index female member to be deleted
        		(bind ?idxDelete -1)
        		(while (or (< ?idxDelete 0) (> ?idxDelete ?*countFemale*))
            		(printout t "Which member to be deleted [1.." ?*countFemale* " | 0 back to main menu]: ")
            		(bind ?idxDelete (read))
            		
            		(
                		if(eq (integerp ?idxDelete) FALSE) then
                		(bind ?idxDelete -1)
                	)
            	)
        
            	;Delete female member based on index
        		(
            		if (neq ?idxDelete 0) then
            			(bind ?*countFemale* 0)
            			(assert (deleteFemale ?idxDelete))
						(run)
            
            			(printout t "Female member with id: " ?idxDelete " => successfully deleted!" crlf)
		        		(printout t "Press ENTER to continue ...")
		        		(readline)
            	)
        )
   		(break)
    ) 
)

(deffunction menu5()
    ;Input and validate user name
	(bind ?name "")
	(while (or (< (str-length ?name) 3) (> (str-length ?name) 20))
		(printout t "Input your name [3 - 20 characters length]: ")
		(bind ?name (readline))
	)	

    ;Input and validate user gender
	(bind ?gender "")
	(while (and (neq ?gender "Male") (neq ?gender "Female"))
		(printout t "Input your gender [ Male | Female ](CASE-SENSITIVE): ")
		(bind ?gender (readline))
	)	

    ;Input and validate user interest
	(bind ?interest "")
	(while (and (neq ?interest "Male") (neq ?interest "Female"))
		(printout t "Input your relationship preference [ Male | Female ](CASE-SENSITIVE): ")
		(bind ?interest (readline))
	)

    ;Input and validate user age
	(bind ?age 0)
	(while (or (< ?age 16) (> ?age 80))
		(printout t "Input your age [16 - 80](years): ")
		(bind ?age (read))
		
		(
    		if (eq (integerp ?age) FALSE) then
    			(bind ?age 0)
    	)
	)

    ;Input and validate user height
	(bind ?height 0)
	(while (or (< ?height 100) (> ?height 240))
		(printout t "Input your height [100 - 240](cm): ")
		(bind ?height (read))
		
		(
    		if (eq (integerp ?height) FALSE) then
    			(bind ?height 0)
    	)
	)

    ;Input and validate user hobby
	(bind ?hobby "")
	(while (and (and (neq ?hobby "Sport") (neq ?hobby "Music")) (neq ?hobby "Game"))
		(printout t "Input your hobby [ Sport | Music | Game ](CASE-SENSITIVE): ")
		(bind ?hobby (readline))
	)

    ;Input and validate user preferred income (-1 if interest is Female)
    (bind ?preferredIncome -1)
	(
    	if (eq ?interest "Male") then
    		(while (or (< ?preferredIncome 0) (> ?preferredIncome 10000))
        		(printout t "Input preferred income [0 - 10000]($USD): ")
        		(bind ?preferredIncome (read))
        		
        		(
            		if (eq (integerp ?preferredIncome) FALSE) then
            			(bind ?preferredIncome -1)
            	)
        	)
    )

	;Insert user profile to facts
    (assert (matchUser (name ?name) (age ?age) (gender ?gender) (height ?height) (hobby ?hobby) (interest ?interest) (preferredIncome ?preferredIncome)))
    
    ;Search match based on interest
    (
    	if(eq ?interest "Male") then
        	(assert (searchMale))
        	(run)
        elif (eq ?interest "Female") then
        	(assert (searchFemale))
    		(run)
    )

    ;Graphical User Interface
    ;(facts)
    (new Template)

    ;Retract all defrule for chaining, all match member, and user profile
    (
    	if(eq ?interest "Male") then
        	(assert (searchMale-retractUser))
		    (run)
		    (retract-string "(searchMale-done)")
        elif (eq ?interest "Female") then
        	(assert (searchFemale-retractUser))
		    (run)
		    (retract-string "(searchFemale-done)")
    )
    
	(readline)
    ;(facts)
)

;DEFQUERY
(defquery matchUserQuery
    ;(declare (variables ))
    (matchUser (name ?name) (age ?age) (gender ?gender) (height ?height) (hobby ?hobby) (interest ?interest) (preferredIncome ?preferredIncome))
)

(defquery matchMaleQuery
    ;(declare (variables ))
    (matchMale (name ?name) (age ?age) (hobby ?hobby) (interest ?interest) (height ?height) (income ?income)(match-rate ?match-rate))
)

(defquery matchFemaleQuery
    ;(declare (variables ))
    (matchFemale (name ?name) (age ?age) (hobby ?hobby) (interest ?interest) (height ?height)(match-rate ?match-rate))
)

;Insert deffacts
(reset)

;MAIN
(bind ?choose 0)
(while (neq ?choose 6)
    (clearScreen)
    (printout t "==========" crlf)
    (printout t "| TICDER |" crlf)
    (printout t "==========" crlf)
    (printout t "1. View Members" crlf)
	(printout t "2. Add a New Member" crlf)
	(printout t "3. Update Member’s Profile" crlf)
	(printout t "4. Delete Member" crlf)
	(printout t "5. Search Match" crlf)
	(printout t "6. Exit" crlf)
    
    (bind ?choose 0)
    (while (or (< ?choose 1)(> ?choose 6))
        (printout t ">> Input [1-6]: ")
    	(bind ?choose (read))
        
        (
        	if(eq (numberp ?choose) FALSE) then
        		(bind ?choose 0)
    	)
    )
    
    (
        if(eq ?choose 1) then
    		(menu1)
        elif(eq ?choose 2) then
        	(menu2)
        elif(eq ?choose 3) then
        	(menu3)
        elif(eq ?choose 4) then
        	(menu4)
        elif(eq ?choose 5) then
        	(menu5)
    )
)