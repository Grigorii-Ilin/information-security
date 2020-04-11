#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <locale.h>
#include "mod_ops.h"

int comparer(int a, int b) {
	int tmp;
	while (b > 0 && a > 0) {
		if (b > a) {
			tmp = a;
			a = b;
			b = tmp;
		}
		a = a % b;
	}
	if (b > a)
		return b;
	else
		return a;
}

int get_public(int phi) {
	int public_key;
	int offset = 0;
	public_key = rand() % phi;
	while (comparer(public_key, phi) > 1) {
		offset++;
		public_key = (rand() + offset) % phi;
	}
	return public_key;
}


int main(void) {
	setlocale(LC_ALL, "RUS");

	int p1 = 227, p2 = 31;
	int n = p1 * p2;
	int number = (p1 - 1) * (p2 - 1);
	int publicKey;
	int privateKey;
	int message[6] = { 'M','u','s','i','c',0 };
	int i = 0;
	srand(time(0));
	publicKey = get_public(number);
	privateKey = mod_div(publicKey, number);

	printf("Исходное сообщение:\n");
	for (i = 0; i < 6; i++) {
		printf("%c", (char)message[i]);
	}
	printf("\n");

	printf("Кодирование сообщения:\n");
	for (i = 0; i < 6; i++) {
		message[i] = mod_pow(message[i], publicKey, n);
		printf("%c", (char)('!' + (message[i] % ('}' - '!'))));
	}
	printf("\n");

	printf("Декодирование сообщения:\n");
	for (i = 0; i < 6; i++) {
		message[i] = mod_pow(message[i], privateKey, n);
		printf("%c", (char)message[i]);
	}
	printf("\n");

	printf("Публичный ключ: %d Приватный ключ: %d\n", publicKey, privateKey);

	return 0;
}