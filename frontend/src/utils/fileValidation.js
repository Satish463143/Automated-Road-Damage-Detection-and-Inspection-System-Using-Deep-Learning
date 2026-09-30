import {
  ALLOWED_IMAGE_TYPES,
  MAX_UPLOAD_SIZE_MB,
} from "../config/appConfig";

export function validateRoadImage(file) {
  if (!file) {
    return "Choose an image first.";
  }

  if (!ALLOWED_IMAGE_TYPES.includes(file.type)) {
    return "Only JPG, JPEG, and PNG images are supported.";
  }

  const maxBytes = MAX_UPLOAD_SIZE_MB * 1024 * 1024;

  if (file.size > maxBytes) {
    return `Image must be ${MAX_UPLOAD_SIZE_MB} MB or smaller.`;
  }

  return null;
}
