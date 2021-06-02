!=======================================================================
!  READ_KCB, Subroutine, Zachary Zambreski, 05/2021
!  Read  dailycrop coefficients records into array. 
!  Only needs to be called once.
!-----------------------------------------------------------------------
!  REVISION HISTORY
!  --NONE
!-----------------------------------------------------------------------
!  Called by: IPWTH
!  Calls:     ModuleDef functions
!=======================================================================

	  SUBROUTINE READ_KCB(CONTROL,YRDOY_A,KCB_A)
	
	    USE ModuleDefs
	
		INTEGER, PARAMETER :: MaxRecords = 10000
		INTEGER, DIMENSION(MaxRecords) :: YRDOY_A_KCB, LineNumber,YRDOY_A
		INTEGER LastRec, LastWeatherDay, NRecords,LUNIO,FirstWeatherDay
		REAL, DIMENSION(MaxRecords) :: KCB_A
		INTEGER CENTURY, ERR, ErrCode, FOUND, LINKCB, LUNKCB, MULTI, RUN,ISECT ,C1,C2,YRDOYW 
		CHARACTER*12 FILEKC,ERRKEY
		CHARACTER*120 LINE
		CHARACTER*30 FILEIO
		REAL KCB
		PARAMETER (ERRKEY = 'IPKCB ')
		
		
		TYPE (ControlType) CONTROL
		
		LUNIO  = CONTROL % LUNIO
        FILEIO = CONTROL % FILEIO  		
		
		! Open the DSAST.INP file. Get name of KCB file
		OPEN (LUNIO, FILE = FILEIO,STATUS = 'OLD',IOSTAT=ERR)
		READ (LUNIO,'(12(/),15X,A12,1X,A80)',IOSTAT=ERR) FILEKC, PATHKC
		
		! Intialize arrays/integers
		NRecords     = 0
        YRDOY_A_KCB  = 0
	    KCB_A        = 0.0
		LUNKCB       = 100
		LINKCB       = 1
		
		! COLUMNS WITH DATA
		C1 = 9
		C2 = 13
		
		! OPEN THE DATA FILE WITH KCB
		OPEN (LUNKCB,FILE=FILEKC,STATUS='OLD',IOSTAT=ERR)
		IF (ERR .NE. 0) THEN
			CALL ERROR (ERRKEY,1,FILEKC,LINKCB)! End of file 
		ENDIF
		 
		! Look for the header line
		CALL IGNORE2 (LUNKCB, LINKCB, ISECT, LINE)
		
		DO WHILE (.TRUE.)   !.NOT. EOF(LUNWTH)
          CALL IGNORE2 (LUNKCB, LINKCB, ISECT, LINE)
          SELECT CASE(ISECT)
			  CASE(0); CALL ERROR (ERRKEY,10,FILEKC,LINKCB)!End of file 
			  CASE(1)
				IF(FirstWeatherDay .EQ. -99) THEN
				  CALL ERROR (ERRKEY,2,FILEKC,LINKCB)      !Data record 
				ENDIF
			  CASE(2); CYCLE                               !End of section 
			  CASE(3); EXIT                                !Header line 
          END SELECT
        ENDDO
		
		! Iterate each line of data
		! Read array of KCB records for this calendar year 
		! starting with simulation start date and ending at end 
		! of file or at MaxRecords # of records
		
		DO WHILE (.TRUE.)   !.NOT. EOF(LUNWTH)
			CALL IGNORE(LUNKCB,LINKCB,FOUND,LINE)		
			IF (FOUND == 1) THEN
		
				READ(LINE,'(I5)',IOSTAT=ERR)   YRDOYW
				READ(LINE(C1:C2),*,IOSTAT=ERR) KCB
				
				IF (ERR .NE. 0) KCB = -99.
				
				IF ((KCB .LT. 0) .OR. (KCB .GT. 2)) THEN
					CALL ERROR (ERRKEY,3,FILEKC,LINKCB)
				ENDIF
				
				IF (NRecords == 0) THEN
					FirstWeatherDay = YRDOYW
				ENDIF

				! ASSIGN PARSED VALUE INTO ARRAY
				NRecords = NRecords + 1
				YRDOY_A_KCB(NRecords) = YRDOYW
				KCB_A(NRecords)  = KCB
			ELSE
			   EXIT ! Exit the loop if no more lines
			ENDIF
			
		ENDDO
    
	End Subroutine READ_KCB
