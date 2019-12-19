#include<stdio.h>
#include<string.h>
#include<stdlib.h>

struct Data{
	char temp;
	Data *next;
}*head,*tail,*curr;

typedef struct Data stack;

void frontPush(char ch){
	stack *newNode=(stack*)malloc(sizeof(stack));
	newNode->temp=ch;
	newNode->next=NULL;
	if(head){
		newNode->next=head;
		head=newNode;
	}else{
		head=tail=newNode;
	}
}

void frontPop(){
	curr=head;
	if(curr){
		if(head==tail){
			head=tail=NULL;
		}else{
			head=head->next;
			free(curr);
		}
	}
}

int priority(char ch){
	if(ch=='+'||ch=='-') return 1;
	else if(ch=='*'||ch=='/') return 2;
	else return 0;
}

void infixToPostfix(char infix[]){
	int i=0, len;
	char a, b;
	
	len=strlen(infix);

	while(i<len){
		a = infix[i];
		if(a>47 && a<58) putchar(a);
		else if(a=='(') frontPush(a);
		else if(a==')'){
			curr=head;
			while(curr && curr->temp!='('){
				putchar(curr->temp);
				frontPop();
				curr=head;
			}
			frontPop();
		}
		else{
			if(!head) frontPush(a);
			else{
				while(head && priority(head->temp)>=priority(a)){
					putchar(head->temp);
					frontPop();
				}
				frontPush(a);
			}
		}
		i++;
	}

	curr=head;
	while(curr){
		putchar(curr->temp);
		frontPop();
		curr=head;
	}
	putchar('\n');
}

int main(){
	int cases, i, flag=0;
	char ch, infix[100];

	scanf("%d", &cases); getchar();getchar();

	while(cases--){
		i=0;
		while((ch=getchar())!=EOF && ch!='\n'){
			infix[i]=ch;
			i++;
			getchar();
		}
		infix[i]='\0';

		if(flag==1) putchar('\n');
		flag=1;

		infixToPostfix(infix);

		head=tail=NULL;
	}	
	return 0;
}