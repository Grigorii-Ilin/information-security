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
    printf("%s", key);

    printf("%s", "Введите текст для шифрования (A-Z):\n");
    char txt[255];
    scanf_s("%254s", txt, 255);
    printf("%s", txt);

    //char result[255];
    encrypt(key, strlen(key), txt, strlen(txt));//, result);
    printf("%s", txt);


    return 0;
}