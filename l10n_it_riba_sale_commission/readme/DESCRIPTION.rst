**Italiano**

Il modulo permette di integrare il pagamento RiBa con le provvigioni agenti.

Nella generazione delle provvigioni agente, una fattura con termini di pagamento
RiBa ed emissione con tipologia "Salvo buon fine" verrà presa in considerazione
solamente trascorsi il numero di giorni impostati nel campo "Giorni di sicurezza"
nella configurazione RiBa.
Il filtro per la data di pagamento, nel caso di un pagamento Riba, scarterà tutti
i pagamenti dove non sono passati almeno i "Giorni di sicurezza" rispetto alla
data di scadenza.

È possibile impostare la spunta su "Senza provvigioni" nelle fatture, in modo
che non vengano generate provvigioni agente.

Le fatture con pagamento RiBa verranno prese in considerazione solo se è passato un dato numero di giorni
(impostati nel campo "Giorni di sicurezza per provvigioni" nella Configurazione RiBa) tra la scadenza del
pagamento RiBa e la "Data pagamento fino a" impostata nella procedura guidata delle liquidazioni agenti.

Es:

- Fattura 0001 è pagata con RiBa
- Scadenza pagamento RiBa: 01/01
- "Giorni di sicurezza per le provvigioni" impostato in configurazione RiBa: 10
- Nella procedura guidata liquidazioni agente:
    - Liquida provvigioni con "Data pagamento fino a" = 05/01 => il pagamento viene ignorato nel calcolo delle provvigioni da liquidare
    - Liquida provvigioni con "Data pagamento fino a" = 15/01 => il pagamento viene considerato nel calcolo delle provvigioni da liquidare

**English**

The module allows you to integrate the RiBa payment with agent commissions.

When generating agent commissions, an invoice with RiBa
payment terms and "Subject To Collection" type issue will be taken
into consideration only after the number of days set in the "Safety Days" field
in RiBa configuration.
The payment date filter, in the case of a Riba payment, will exclude all payments
where at least the "Safety Days" have not passed from the due date.

It is possible to set "Without commissions" flag in invoices, in this way
no agent commissions are generated.

When generating agent settlements, select a payment date until which commissions should be settled.

Invoices with RiBa payment will be taken into consideration only if enough days (set in the
"Safety days for commission" field in RiBa configuration) have passed between the "due date"
of the RiBa payment and the payment date set in the settlement wizard.

Eg:

- Invoice 0001 is paid with RiBa
- RiBa due date: January 1st
- "Safety days for commission" set in RiBa configuration: 10
- In settlement wizard:
    - Settle commissions until payment date: January 5th => commission is not settled for RiBa
    - Settle commissions until payment date: January 15th => commission is settled for RiBa
