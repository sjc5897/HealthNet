#include <stdio.h>

struct test1{
	unsigned int :3;
	unsigned int :2;
	unsigned int f1:4;
	unsigned int f2:7;
	unsigned int f3:5;
	unsigned int f4:6;
}test1;

int main(){
	if(sizeof(int *) == 8){
		printf("%d-bit system\n", 64);
	}
	else{
		printf("%d-bit system\n", 32);
	}
	printf("Size: %lu bytes\n", sizeof(test1));
	return 0;
}
