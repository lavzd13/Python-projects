void	calculate_combs() {
int	digit1 = 0;
int	digit2 = 0;
int	digit3 = 0;
int	digit4 = 0;
char	combs[10001][4];
int count = 0;

while (1) {
	combs[count][0] = digit1 + '0', combs[count][1] = digit2 + '0', combs[count][2] = digit3 + '0', combs[count][3] = digit4 + '0';
	count++;
	if (digit4 == 9 && digit3 == 9 && digit2 == 9 && digit1 == 9)
		break;
	digit4++;
	if (digit4 == 10) {
		digit3++;
		digit4 = 0;
	}
	if (digit3 == 10) {
		digit2++;
		digit3 = 0;
		digit4 = 0;
	}
	if (digit2 == 10) {
		digit1++;
		digit2 = 0;
		digit3 = 0;
		digit4 = 0;
	}
};
}

int main(void) {
	calculate_combs();
}