#include <stdlib.h>   
#include <string.h>     

extern "C"{

// Структура узла очереди
typedef struct Node {
    int a;              
    char b[21];         
    struct Node* next;  // Указатель на следующий элемент в очереди
} Node;

// Структура очереди
typedef struct Queue {
    Node* front;        // Указатель на первый элемент
    Node* rear;         // Указатель на последний элемент
    int size;           // Кол-во элементов в очереди
    int created;        // Флаг
} Queue;

Queue* createQueue(){
    Queue* q = (Queue*)malloc(sizeof(Queue));
    q->front=NULL;
    q->rear=NULL;
    q->size=0;
    q->created=1;
    return q;
}

// Очистка очереди
void clearQueue(Queue* q) {
    if (q == NULL) return;
    // Проходим по всем узлам и освобождаем память
    while (q->front != NULL) {
        Node* temp = q->front;        // Сохраняем текущий узел
        q->front = q->front->next;    // Перемещаем указатель на следующий
        free(temp);                   // Освобождаем память узла
    }
    q->rear = NULL;   
    q->size = 0;
    q->created = 0;       
}

// Добавление элемента
void enqueue(Queue* q, int a, char* b) {
    if (q == NULL) return;
    // Выделяем память под новый узел
    Node* newNode = (Node*)malloc(sizeof(Node));

    // Заполняем данные нового узла
    newNode->a = a;                
    strcpy(newNode->b, b);         
    newNode->next = NULL;          // Новый узел — последний

    // Если очередь пуста — новый узел становится и первым, и последним
    if (q->rear == NULL) {
        q->front = q->rear = newNode;
    } else {
        // Иначе добавляем в конец
        q->rear->next = newNode;   // Предыдущий последний теперь ссылается на новый
        q->rear = newNode;         // Новый узел становится последним
    }
    q->size++; // Увеличиваем счётчик элементов
}

// Удаление элемента из начала очереди (dequeue)
int dequeue(Queue* q,int* out_a,char* out_b) {
    if (q == NULL || q->front == NULL) {
        return 0;
    }

    // Сохраняем указатель на удаляемый узел
    Node* temp = q->front;

    *out_a = temp->a;
    strcpy(out_b,temp->b);


    // Перемещаем начало очереди на следующий элемент
    q->front = q->front->next;

    // Если после удаления очередь стала пустой — обнуляем хвост
    if (q->front == NULL) {
        q->rear = NULL;
    }

    // Освобождаем память удалённого узла
    free(temp);
    q->size--; // Уменьшаем счётчик

    return 1;
}
}