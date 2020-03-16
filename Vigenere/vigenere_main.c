#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <locale.h>
#include "vigenere_lib.h"


int main(){
    setlocale(LC_ALL, "RUS");

    printf("%s", "Введите пароль (A-Z):\n");
    char key[255];
    scanf_s("%254s", key, 255);
    printf("%s\n", key);

    printf("%s", "Введите текст для шифрования (A-Z):\n");
    char txt[255];
    scanf_s("%254s", txt, 255);
    printf("%s\n", txt);

    encrypt(key, strlen(key), txt, strlen(txt));
    printf("Зашифровано: %s\n", txt);

    decrypt(key, strlen(key), txt, strlen(txt));
    printf("Расшифровано: %s\n", txt);

    return 0;
}