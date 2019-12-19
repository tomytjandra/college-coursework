#include<stdio.h>
#include<stdlib.h>

struct Edge{
	int x, y, v;
}D[150000], E[150000];
int p[550], r[550];

void initialize(int n){
	for(int i=0; i<=n; i++){
		p[i] = i;
		r[i] = 1;
	}
}

void sort(int n){
	int a[40]={};
	for(int i=0; i<n; i++) a[D[i].v]++;
	for(int i=1; i<40; i++) a[i] = a[i]+a[i-1];
	for(int i=0; i<n; i++) E[--a[D[i].v]] = D[i];
}

int findParent(int x){
	if(p[x]==x) return x;
	else return p[x]=findParent(p[x]);
}

int joint(int x, int y){
	x = findParent(x);
	y = findParent(y);
	
	if(x!=y){
		if(r[x]<=r[y]){
			p[x] = y;
			r[y] = r[x]+r[y];
		}else{
			p[y] = x;
			r[x] = r[x]+r[y];
		}
		return 1;
	}
	return 0;
}

int main(){
	int T, N, temp, sum, cases;
	char lock[550][5] = {"0000"};
	
	scanf("%d", &T);

	while(T--){
		cases=0;
		scanf("%d", &N);
		
		for(int i=1; i<=N; i++){
			scanf("%s", lock[i]);
			
			for(int j=1; j<i; j++){
				sum=0;

				for(int k=0; k<4; k++){
					temp = abs(lock[i][k]-lock[j][k]);
					
					if(temp>5) temp = 10-temp;
					sum = sum+temp;
				}
				D[cases].x = i;
				D[cases].y = j;
				D[cases].v = sum;
				cases++;
			}
		}
		sort(cases);
		initialize(N);

		int answer=0, counter=0, l=40;
		
		for(int i=0; i<cases; i++){
			if(joint(E[i].x, E[i].y)){
				answer = answer+E[i].v;
				counter++;
				
				if(counter == N) break;
			}
		}
		
		for(int i=1; i<=N; i++){
			sum=0;
			for(int j=0; j<4; j++){
			temp = abs(lock[0][j]-lock[i][j]);
				
				if(temp>5) temp=10-temp;
				sum = sum+temp;
			}
			
			if(l>sum) l = sum;
		}
		
		printf("%d\n", answer+l);
	}
	return 0;
}