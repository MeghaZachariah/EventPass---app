function viewEvent(eventId) {
    // store selected event
    localStorage.setItem("event_id", eventId);

    // go to event page
    window.location.href = "event.html";
}