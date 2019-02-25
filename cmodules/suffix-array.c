#include <stdio.h>
#include <stdlib.h>
#include "divsufsort.h"

int main(int argc, char* argv[])
{
	if(argc<3)
	{
		printf("Usage: %s INPUT_FILE_PATH OUTPUT_FILE_PATH\n",argv[0]);
		exit(1);
	}
	
	FILE* f = fopen(argv[1],"r");
	if(f==NULL)
	{
		printf("Error reading file\n");
		exit(1);
	}
	
	size_t fileSize;
	fseek(f,0,SEEK_END);
	fileSize = ftell(f);
	rewind(f);

	char* inText = (char*) malloc(fileSize);
	if(inText==NULL) 
	{
		printf("Error allocating buffer\n");
		exit(1);
	}

	
	fread(inText,1,fileSize,f);
	fclose(f);

	char* outText = (char*) malloc(fileSize);
	
	divbwt(inText,outText,NULL,fileSize);

	FILE* fout = fopen(argv[2],"w");
	fwrite(outText,1,fileSize,fout);
	fclose(fout);

	return 0;
}
