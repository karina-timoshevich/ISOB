#include <stdio.h>
#include <string.h>

void vulnerable() {
    char buffer[10];
    printf("[Уязвимая версия] Введите данные: ");
    fflush(stdout);
    gets(buffer);
    printf("Вы ввели: %s\n", buffer);
    fflush(stdout);
}

int main() {
    vulnerable();
    return 0;
}