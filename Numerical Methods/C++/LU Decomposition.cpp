#include<stdio.h>

int main(){
	int n, i, j, k;
	float A[10][10], b[10], bTemp[10], sol[10], solTemp[10], L[10][10]={0}, temp, lValue;

	/*Minta inputan*/
	do{
		printf("How many variable(s) [2~10]: ");
		scanf("%d",&n); getchar();
	}while(n<2||n>10);

	/*Memasukkan value ke dalam matrix A dan b*/
	for(i=0;i<n;i++){
		printf("\n============\n");
		printf("EQUATION #%d\n",i+1);
		printf("============\n");
		for(j=0;j<n;j++){
			printf("Coef. of x%d: ",j+1);
			scanf("%f",&A[i][j]); getchar();
			if(j==n-1){
				printf("RHS Value: ");
				scanf("%f",&b[i]); getchar();
				bTemp[i] = b[i];
			}
		}
	}
	
	/*OBE penukaran baris apabila diagonal utama = 0*/
	for(i=0;i<n;i++){
		if(A[i][i]==0){
			for(j=i+1;j<n;j++){
				if(A[j][i]!=0){
					for(k=0;k<n;k++){
						/*Swap baris untuk matrix A*/
						temp = A[i][k];
						A[i][k] = A[j][k];
						A[j][k] = temp;
					}
					/*Swap baris untuk matrix b*/
					temp = b[i];
					b[i] = b[j];
					b[j] = temp;
				}
			}
		}
	}
   
	/*Matrix L*/
	for(i=0;i<n;i++){
		for(j=i+1;j<n;j++){
			if(A[j][i]!=0){
				lValue = A[j][i]/A[i][i];
				for(k=0;k<n;k++)
				{
					A[j][k] = A[j][k]-(A[i][k]*lValue);
				}
				b[j] = b[j]-(b[i]*lValue);
				L[j][i] = lValue;
			}
		}
	}
	
	/*Diagonal utama matrix L pasti bernilai 1*/
	for(i=0;i<n;i++){
		L[i][i]=1;
	}

	/*Menghitung solusi*/
	for(i=0;i<n;i++){
		for(j=0;j<i;j++){
			bTemp[i] = bTemp[i]-(solTemp[j]*L[i][j]);
		}
		solTemp[j] = bTemp[i];
	}
   
	for(i=n-1;i>=0;i--){
		for(j=n-1;j>i;j--){
			solTemp[i] = solTemp[i]-(sol[j]*A[i][j]);
		}
		sol[j] = solTemp[i]/A[j][j];
	}
   
	/*Print out solusi*/
	printf("\n============\n");
	printf("SOLUTION\n");
	printf("============\n");
	for(i=0;i<n;i++){
		printf("Solution for x%d is %.2f\n",i+1,sol[i]);
	}

	/*Print out matrix L*/
	printf("\n============\n");
	printf("MATRIX L\n");
	printf("============\n");
	for(i=0;i<n;i++){
		for(j=0;j<n;j++){
			printf("%7.2f ",L[i][j]);
		}
		printf("\n");
	}

	/*Print out matrix U*/
	printf("\n============\n");
	printf("MATRIX U\n");
	printf("============\n");
	for(i=0;i<n;i++){
		for(j=0;j<n;j++){
			printf("%7.2f ",A[i][j]);
		}
		printf("\n");
	}
   
   getchar();
   return 0;
}