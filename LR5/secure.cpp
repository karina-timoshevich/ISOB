#include <stdio.h>
#include <string.h>

#define BUFFER_SIZE 10

void secure() {
    char buffer[BUFFER_SIZE];
    char input[BUFFER_SIZE * 2];

    printf("[Защищенная версия] Введите данные: ");
    fflush(stdout);

    if (fgets(input, sizeof(input), stdin) == NULL) {
        printf("Ошибка ввода!\n");
        return;
    }
    input[strcspn(input, "\n")] = '\0';

    if (strlen(input) >= BUFFER_SIZE) {
        printf("Ошибка: ввод слишком длинный (макс. %d символов)!\n", BUFFER_SIZE - 1);
        fflush(stdout);
        return;
    }

    strncpy(buffer, input, BUFFER_SIZE - 1);
    buffer[BUFFER_SIZE - 1] = '\0';

    printf("Буфер содержит: %s\n", buffer);
    fflush(stdout);
}

int main() {
    secure();
    return 0;
}