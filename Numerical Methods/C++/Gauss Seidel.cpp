#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/*Function untuk mengedit persamaan*/
int repeat(int indicator)
{
	if(indicator==1) return 1;
	else
	{
		char repeat;
		printf("\n\nInsert again ? (y/n) ");scanf("%c",&repeat);fflush(stdin);
		if(repeat=='y')return 1;
		else return 0;
	}
}

/*Function untuk mencetak persamaan satu per satu*/
void printOneEquation(float Matrix[10][11], int numberOfVariable, int numberOfEquation)
{
	int idx2;
	
	for(idx2=0;idx2<numberOfVariable+1;idx2++)
	{
		printf("%3.0f ",Matrix[numberOfEquation][idx2]);
		
		if(idx2<numberOfVariable)printf("y%d",idx2+1);
		if(idx2<numberOfVariable-1)printf (" + ");
		if(idx2==numberOfVariable-1)printf (" = ");
	}
}

/*Function untuk memvalidasi diagonally dominant untuk setiap persamaan*/
bool isDiagonallyDominantPerEquation(float Matrix[10][11], int numberOfVariable, int numberRow)
{
	float max=0;
	
	int maxIdx;
	
	int idx2;
	
	for(int idx2=0;idx2<numberOfVariable;idx2++)
	{
		if(fabs(Matrix[numberRow][idx2]) >= max && idx2<=numberRow)
		{
			max = fabs(Matrix[numberRow][idx2]);
			maxIdx=idx2;	
		}
	}
	
	if(numberRow==maxIdx)return true;
	else return false;
}

/*Function untuk memvalidasi diagonally dominant secara keseluruhan persamaan*/
bool isDiagonallyDominant(float Matrix[10][11],int numberOfVariable)
{
	int idx1;
	
	for(idx1=0;idx1<numberOfVariable;idx1++)
	{
		if(isDiagonallyDominantPerEquation(Matrix,numberOfVariable,idx1)==false) return false;	
	}
	
	return true;
}

/*Function untuk mencetak semua persamaan*/
void printEquations(float Matrix[10][11], int numberOfVariable)
{
	int idx1,idx2;
	for(idx1=0;idx1<numberOfVariable;idx1++)
	{
		printf("Equation-%d\n\n",idx1+1);
		for(idx2=0;idx2<numberOfVariable+1;idx2++)
		{
			printf("%3.0f ",Matrix[idx1][idx2]);
			
			if(idx2<numberOfVariable)printf("y%d",idx2+1);
			if(idx2<numberOfVariable-1)printf (" + ");
			if(idx2==numberOfVariable-1)printf (" = ");
		}
	
		printf("\n\n\n");
	}
}

int main()
{
	int indicator=0;
	
	int idx1,idx2,idx3;
	
	int numberOfVariable;
	
	float Matrix[10][11]={0};
	
	/*Minta inputan*/
	do
	{
		system("cls");
		printf("Number of variable (min 1 max 10) : ");
		scanf("%d",&numberOfVariable);fflush(stdin);
	}while(numberOfVariable<1 || numberOfVariable>10);
	
	/*Memasukkan value ke dalam matrix*/
	do
	{
		do
		{
			for(idx1=0;idx1<numberOfVariable;idx1++)
			{
				for(idx2=0;idx2<numberOfVariable+1;idx2++)
				{
					system("cls");
					printf("Equation-%d\n\n",idx1+1);
					printOneEquation(Matrix,numberOfVariable,idx1);
					
					printf("\n\n");
					
					if(idx2<numberOfVariable)printf("y%d : ",idx2+1);
					if(idx2==numberOfVariable)printf("value : ");
					scanf("%f",&Matrix[idx1][idx2]);fflush(stdin);
				}
				system("cls");
				printf("Equation-%d\n\n",idx1+1);
				printOneEquation(Matrix,numberOfVariable,idx1);
				
				getchar();
			}
			system("cls");
			printEquations(Matrix,numberOfVariable);
			
			indicator=0;
			indicator=repeat(indicator);
		}while(indicator==1);
		
		if(isDiagonallyDominant(Matrix,numberOfVariable)==false)
		{
			printf("Not Diagonally Dominant!!!");
			getchar();
			printf("Input again!!");
			getchar();
		}
	}while(isDiagonallyDominant(Matrix,numberOfVariable)==false);
	
	float y[10];
	
	float ySol[10];
	
	for(int idx1=0;idx1<numberOfVariable;idx1++) y[idx1] = 0;
	
	float yDivergentSol[10]={0};
	
	int countSame[10]={0};
	
	int numVarDivergent=0;
	
	int indexIteration=0;
	
	printf("\n\n");
	/*Menghitung solusi dengan cara Gauss Seidel*/
	while(true)
	{
		for(int idx1=0;idx1<numberOfVariable;idx1++)
		{
			ySol[idx1] = Matrix[idx1][numberOfVariable];
			
			for(int idx2=0;idx2<numberOfVariable;idx2++)
				if(idx2!=idx1) ySol[idx1] = ySol[idx1] -  Matrix[idx1][idx2]*y[idx2];
			
			ySol[idx1] = ySol[idx1]/Matrix[idx1][idx1];
			
			if(yDivergentSol[idx1] == ySol[idx1])countSame[idx1]++;
			else yDivergentSol[idx1] = ySol[idx1];
		}
		
		printf("%Iteration-%d\t",indexIteration+1);
		
		indexIteration++;
		
		for(int idx1=0;idx1<numberOfVariable;idx1++)
		{
			y[idx1] = ySol[idx1];
			printf("%4.2f ",ySol[idx1]);
		}
		
		printf("\n");
		
		numVarDivergent = 0;
		
		for(int idx1=0;idx1<numberOfVariable;idx1++)
		{
			if(countSame[idx1]>5)numVarDivergent++;
		}
		
		if(numVarDivergent == numberOfVariable)break;
	}
	
	//system("cls");
	
	/*Mencetak persamaan beserta solusinya*/

	//printEquations(Matrix,numberOfVariable);
	
	printf("\n\n\nThe solution : \n\n");
	
	for(int idx1=0;idx1<numberOfVariable;idx1++)
	{
		printf("y%d = %4.2f\n",idx1+1,ySol[idx1]);
	}
	getchar();
	return 0;
}
