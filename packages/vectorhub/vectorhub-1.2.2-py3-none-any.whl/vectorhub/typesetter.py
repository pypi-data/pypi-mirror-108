"""
Converter class to convert into native python objects.
"""
import warnings

class TypeSetter:
    def convert_to_list(self, model_output, method_type='encode'):
        if method_type == 'encode':
            return self.convert_encode_output_to_list(model_output)
        if method_type_ == 'bulk_encode':
            return self.convert_bulk_encode_output_to_list(model_output)
    
    def convert_encode_output_to_list(self, model_output):
        if hasattr(model_output, 'cpu'):
            if hasattr(model_output, 'detach'):
                return model_output.cpu().detach().numpy().tolist()[0]
            if hasattr(model_output, 'numpy'):
                return model_output.cpu().numpy().tolist()[0]
        elif hasattr(model_output, 'numpy'):
            return model_output.numpy().tolist()[0]
        elif hasattr(model_output, 'detach'):
            return model_output.detach().tolist()[0]
        elif hasattr(model_output, 'tolist'):
            return model_outputs.tolist()[0]
        warnings.warn("Unsure how to turn into a list, returning model output as is.")
        return model_outputs
    
    def convert_bulk_encode_output_to_list(self, model_output):
        if hasattr(model_output, 'cpu'):
            if hasattr(model_output, 'detach'):
                return model_output.cpu().detach().numpy().tolist()
            if hasattr(model_output, 'numpy'):
                return model_output.cpu().numpy().tolist()
        elif hasattr(model_output, 'numpy'):
            return model_output.numpy().tolist()
        elif hasattr(model_output, 'detach'):
            return model_output.detach().numpy().tolist()
        elif hasattr(model_output, 'tolist'):
            return model_outputs.tolist()
        warnings.warn("Unsure how to turn into a list, returning model output as is.")
        return model_outputs
