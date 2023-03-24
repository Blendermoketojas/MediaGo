export function hasListener(eventBus, eventName) {
  const allListeners = eventBus.all || eventBus._all; // Use '_all' for mitt
  return allListeners && allListeners.has(eventName);
}
